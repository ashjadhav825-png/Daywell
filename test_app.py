"""
DayWell Test Suite
Verifies API endpoints, privacy guarantees, error handling,
and compliance with the hackathon's no-diagnosis rules.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import os

from app import app, SYSTEM_INSTRUCTION
from knowledge_base import KNOWLEDGE_BASE


class DayWellTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_index_page(self):
        """Verify the single-page application loads with status 200 and required elements."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        self.assertIn("DayWell", html)
        self.assertIn("Habit Tracker", html)
        self.assertIn("Wellness Guide", html)
        self.assertIn("Trusted Sources", html)
        # Verify emergency notice is present
        self.assertIn("In a medical emergency", html)

    def test_config_status_unconfigured(self):
        """Verify /api/config-status reports false when GEMINI_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.get("/api/config-status")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertFalse(data.get("configured"))
            self.assertIn("notice", data)

    def test_config_status_configured(self):
        """Verify /api/config-status reports true without leaking the actual key value."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "AIzaSyFakeTestKeyForTesting12345"}):
            response = self.client.get("/api/config-status")
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data.get("configured"))
            # Make sure the secret key is NOT in the JSON response
            self.assertNotIn("AIzaSyFakeTestKeyForTesting12345", json.dumps(data))

    def test_knowledge_base_endpoint(self):
        """Verify the knowledge base returns structured items from WHO and FSSAI."""
        response = self.client.get("/api/knowledge-base")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get("status"), "success")
        items = data.get("data", [])
        self.assertGreaterEqual(len(items), 5)

        # Check for WHO and FSSAI presence
        orgs = [item["organization"] for item in items]
        has_who = any("WHO" in org for org in orgs)
        has_fssai = any("FSSAI" in org for org in orgs)
        self.assertTrue(has_who, "WHO must be cited in knowledge base")
        self.assertTrue(has_fssai, "FSSAI must be cited in knowledge base")

        # Verify all sources have genuine https:// URLs
        for item in items:
            self.assertIn("sources", item)
            for src in item["sources"]:
                self.assertTrue(src["url"].startswith("https://"))

    def test_chat_unconfigured_key_behavior(self):
        """When API key is missing, chat must return clear instructions without faking responses."""
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post(
                "/api/chat",
                data=json.dumps({"message": "What is the recommended salt intake?"}),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data.get("status"), "unconfigured")
            self.assertIn("Gemini API key is not configured", data.get("message", ""))
            self.assertIn("instructions", data)

    def test_chat_empty_payload(self):
        """Verify validation rejection on empty message."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"}):
            response = self.client.post(
                "/api/chat",
                data=json.dumps({"message": ""}),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn("error", data)

    def test_chat_oversized_payload(self):
        """Verify validation on oversized messages (preventing prompt abuse)."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"}):
            oversized_text = "A" * 2000
            response = self.client.post(
                "/api/chat",
                data=json.dumps({"message": oversized_text}),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)

    @patch("requests.post")
    def test_chat_successful_mocked_gemini(self, mock_post):
        """Verify chat proxying and response handling when Gemini returns 200."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "According to the [WHO Healthy Diet Fact Sheet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet), adults should limit salt to under 5g per day."
                            }
                        ]
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-valid-key"}):
            response = self.client.post(
                "/api/chat",
                data=json.dumps({"message": "How much salt can I eat per day?"}),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data.get("status"), "success")
            self.assertIn("WHO Healthy Diet Fact Sheet", data.get("reply"))

    def test_safety_guardrails_in_system_prompt(self):
        """Verify the system instruction enforces all hackathon no-diagnosis rules."""
        self.assertIn("NO DIAGNOSIS", SYSTEM_INSTRUCTION)
        self.assertIn("NO MEDICINES", SYSTEM_INSTRUCTION)
        self.assertIn("NO PERSONALIZED CARE OR DIET PLANS", SYSTEM_INSTRUCTION)
        self.assertIn("URGENT OR LIFE-THREATENING CONCERNS", SYSTEM_INSTRUCTION)
        self.assertIn("WHO", SYSTEM_INSTRUCTION)
        self.assertIn("FSSAI", SYSTEM_INSTRUCTION)

    def test_frontend_dom_elements_present(self):
        """Verify that all required UI elements and modals exist in the template."""
        with open("templates/index.html", "r", encoding="utf-8") as f:
            html = f.read()

        required_ids = [
            'tab-habits-btn', 'tab-chat-btn', 'tab-kb-btn',
            'habits-panel', 'chat-panel', 'kb-panel',
            'open-suggested-btn', 'open-add-habit-btn',
            'week-column-headers', 'habits-list', 'no-habits-placeholder',
            'today-completion-title', 'today-progress-circle', 'weekly-rate-text',
            'daily-reflection-note', 'save-reflection-btn',
            'api-status-badge', 'missing-key-banner',
            'chat-messages', 'chat-form', 'chat-input-field', 'clear-chat-btn',
            'add-habit-modal', 'edit-habit-modal', 'suggested-modal', 'api-key-modal',
            'kb-grid'
        ]

        for elem_id in required_ids:
            self.assertIn(f'id="{elem_id}"', html, f"Element id='{elem_id}' missing in index.html")

    @patch("requests.post")
    def test_save_and_remove_key(self, mock_post):
        """Test the save-key and remove-key endpoints."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        # Test invalid short key
        resp_bad = self.client.post("/api/save-key", json={"api_key": "short"})
        self.assertEqual(resp_bad.status_code, 400)

        # Test valid key save
        test_key = "AIzaSyFakeKeyForTest1234567890abcdef"
        resp_good = self.client.post("/api/save-key", json={"api_key": test_key})
        self.assertEqual(resp_good.status_code, 200)
        self.assertTrue(resp_good.json.get("success"))
        self.assertEqual(os.environ.get("GEMINI_API_KEY"), test_key)

        # Test remove key
        resp_rem = self.client.post("/api/remove-key")
        self.assertEqual(resp_rem.status_code, 200)
        self.assertTrue(resp_rem.json.get("success"))
        self.assertNotIn("GEMINI_API_KEY", os.environ)


if __name__ == "__main__":
    unittest.main()
