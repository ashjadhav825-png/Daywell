"""
DayWell Knowledge Base
Curated educational summaries grounded exclusively in trusted public health sources:
- World Health Organization (WHO)
- Food Safety and Standards Authority of India (FSSAI)
"""

KNOWLEDGE_BASE = [
    {
        "id": "nutrition_balanced_diet",
        "category": "Nutrition",
        "title": "Healthy Diet & Balanced Nutrition",
        "organization": "WHO & FSSAI",
        "summary": "A balanced, nutrient-rich diet protects against malnutrition and noncommunicable diseases such as diabetes, heart disease, stroke, and cancer. It emphasizes variety, fresh whole foods, and minimal ultra-processed items.",
        "key_points": [
            "Consume at least 400g (approx 5 portions) of fruits and vegetables daily, excluding potatoes and other starchy tubers (WHO).",
            "Limit free sugars to less than 10% of total energy intake (ideally under 5% for additional health benefits) (WHO).",
            "Keep total fat intake under 30% of total energy; shift fat intake away from saturated and industrial trans-fats towards unsaturated fats (WHO).",
            "Keep salt intake under 5 grams per day (roughly 1 teaspoon) and ensure salt is iodized to support thyroid function and cardiovascular health (WHO).",
            "Follow the FSSAI 'Eat Right India' principle: Eat Healthy (less fat, sugar, salt), Eat Safe (hygienic handling), and Eat Sustainably (local, seasonal produce) (FSSAI).",
            "Look for the +F logo on fortified staple foods (milk, oil, wheat flour, rice, and double fortified salt) to help bridge micronutrient gaps (FSSAI)."
        ],
        "sources": [
            {
                "title": "WHO Healthy Diet Fact Sheet",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/news-room/fact-sheets/detail/healthy-diet"
            },
            {
                "title": "FSSAI Eat Right India Initiative",
                "organization": "Food Safety and Standards Authority of India (FSSAI)",
                "url": "https://eatrightindia.gov.in/"
            },
            {
                "title": "WHO Salt Reduction Guidelines",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/news-room/fact-sheets/detail/salt-reduction"
            }
        ]
    },
    {
        "id": "physical_activity",
        "category": "Movement & Physical Activity",
        "title": "Daily Physical Activity & Reducing Sedentary Time",
        "organization": "WHO",
        "summary": "Regular physical activity is proven to help prevent and manage noncommunicable diseases such as heart disease, stroke, diabetes, and several cancers. It also reduces symptoms of depression and anxiety and enhances thinking, learning, and overall well-being.",
        "key_points": [
            "Adults (18-64 years) should undertake at least 150-300 minutes of moderate-intensity aerobic physical activity, or at least 75-150 minutes of vigorous-intensity aerobic physical activity per week, or an equivalent combination (WHO).",
            "Muscle-strengthening activities involving all major muscle groups should be performed on 2 or more days a week (WHO).",
            "Limit the amount of time spent being sedentary. Replacing sedentary time with physical activity of any intensity (even light movement like walking or stretching) provides health benefits (WHO).",
            "Any activity is better than none: simple lifestyle breaks, climbing stairs, and brisk walking all contribute to the weekly activity goal (WHO)."
        ],
        "sources": [
            {
                "title": "WHO Physical Activity Guidelines & Fact Sheet",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/news-room/fact-sheets/detail/physical-activity"
            }
        ]
    },
    {
        "id": "sleep_circadian",
        "category": "Sleep & Rest",
        "title": "Restorative Sleep & Sleep Hygiene",
        "organization": "WHO",
        "summary": "Quality sleep is fundamental to physical health, cognitive performance, metabolic regulation, and emotional resilience. Chronic sleep disruption elevates the risk of cardiovascular conditions, immune dysfunction, and mood disorders.",
        "key_points": [
            "Maintain a consistent sleep-wake schedule, waking up and going to bed at similar times every day, even on weekends (WHO mental well-being guidance).",
            "Create an environment conducive to rest: cool, quiet, well-ventilated, and dark.",
            "Establish a gentle wind-down routine 30-60 minutes before bed: limit exposure to bright screens, avoid heavy meals late at night, and curtail caffeine or stimulants in the evening.",
            "Use daytime natural light exposure to reinforce the natural circadian rhythm."
        ],
        "sources": [
            {
                "title": "WHO Mental Health & Well-being Resources",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response"
            }
        ]
    },
    {
        "id": "stress_management",
        "category": "Mental Well-being & Stress",
        "title": "Coping with Stress & Mindfulness",
        "organization": "WHO",
        "summary": "Stress is a natural human response to challenges and daily demands. Practical, evidence-based coping skills help individuals manage acute and chronic stressors without becoming overwhelmed.",
        "key_points": [
            "Practice 'Grounding': When emotional storms occur, slow down and connect with your physical body (feel feet on the floor, take slow steady breaths, name 5 things you can see around you) (WHO 'Doing What Matters in Times of Stress').",
            "'Unhooking' from difficult thoughts: Notice when you are caught in self-critical or catastrophic thought loops, name the thought ('I notice I am having the thought that...'), and refocus on your immediate actions.",
            "Act on your values: Focus energy on meaningful, constructive behaviors rather than fighting uncontrollable circumstances.",
            "Build social connections: Reaching out to friends, family, or trusted community members offers emotional regulation.",
            "Access professional or crisis counseling whenever distress feels unmanageable (such as national mental health helplines like Tele-MANAS in India at 14416 or 988 in the US)."
        ],
        "sources": [
            {
                "title": "WHO Illustrated Guide: Doing What Matters in Times of Stress",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/publications/i/item/9789240003927"
            }
        ]
    },
    {
        "id": "hygiene_food_safety",
        "category": "Hygiene & Food Safety",
        "title": "Personal Hygiene & Safe Food Handling",
        "organization": "WHO & FSSAI",
        "summary": "Proper hand hygiene and food safety practices represent the most effective barriers against infectious diseases, diarrheal illnesses, and foodborne contamination.",
        "key_points": [
            "Wash hands thoroughly with soap and clean running water for at least 20-30 seconds, covering backs of hands, between fingers, and under nails (WHO).",
            "Key handwashing moments: before preparing or eating food, after using the toilet, after coughing or blowing your nose, and after handling garbage or pets (WHO).",
            "Follow the 5 Keys to Safer Food (WHO & FSSAI): Keep clean, Separate raw and cooked foods, Cook thoroughly (especially meat, poultry, and seafood), Keep food at safe temperatures (below 5°C or above 60°C), and Use safe water and raw materials.",
            "Rinse fresh vegetables and fruits under running water before preparation (FSSAI)."
        ],
        "sources": [
            {
                "title": "WHO Hand Hygiene Recommendations",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/campaigns/world-hand-hygiene-day"
            },
            {
                "title": "WHO Five Keys to Safer Food Manual",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/publications/m/item/five-keys-to-safer-food-manual"
            },
            {
                "title": "FSSAI Food Safety Tips for Consumers",
                "organization": "Food Safety and Standards Authority of India (FSSAI)",
                "url": "https://www.fssai.gov.in/"
            }
        ]
    },
    {
        "id": "ncds_prevention",
        "category": "Prevention & Health Terms",
        "title": "Understanding Noncommunicable Diseases (NCDs)",
        "organization": "WHO",
        "summary": "Noncommunicable diseases (NCDs)—principally cardiovascular diseases (heart attacks and stroke), cancers, chronic respiratory diseases, and diabetes—are the leading causes of mortality globally, but are largely preventable through lifestyle modifications.",
        "key_points": [
            "Modifiable behavioral risk factors: Tobacco use, physical inactivity, unhealthy diet (high in sodium, trans-fats, and sugars), and harmful alcohol use (WHO).",
            "Metabolic risk factors: Elevated blood pressure (hypertension), overweight/obesity, hyperglycemia (high blood glucose), and hyperlipidemia (elevated blood lipids) (WHO).",
            "Cardiovascular disease basics: Diseases affecting the heart and blood vessels; lifestyle prevention includes regular aerobic activity, reducing salt intake, quitting tobacco, and eating plenty of fruits and vegetables (WHO).",
            "Type 2 Diabetes prevention: Moderate physical activity and a balanced diet with whole grains and legumes significantly reduce risk and progression (WHO)."
        ],
        "sources": [
            {
                "title": "WHO Noncommunicable Diseases Fact Sheet",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/news-room/fact-sheets/detail/noncommunicable-diseases"
            },
            {
                "title": "WHO Diabetes Fact Sheet",
                "organization": "World Health Organization (WHO)",
                "url": "https://www.who.int/news-room/fact-sheets/detail/diabetes"
            }
        ]
    }
]

def get_knowledge_base_context_for_prompt() -> str:
    """Format the knowledge base into a concise, authoritative text block for the LLM system prompt."""
    lines = [
        "TRUSTED KNOWLEDGE BASE (Source attribution required for answers):",
        "You must ground your answers in these official facts and cite only the exact URLs provided below.",
        ""
    ]
    for item in KNOWLEDGE_BASE:
        lines.append(f"### Topic: {item['title']} (Organization: {item['organization']})")
        lines.append(f"Summary: {item['summary']}")
        lines.append("Key Guidelines:")
        for pt in item["key_points"]:
            lines.append(f"- {pt}")
        lines.append("Approved Official Sources:")
        for src in item["sources"]:
            lines.append(f"- [{src['title']}]({src['url']}) ({src['organization']})")
        lines.append("")
    return "\n".join(lines)
