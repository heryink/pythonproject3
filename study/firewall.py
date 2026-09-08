import os
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Initialize the Firecrawl Application
# Ensure your API key is set in your environment variables: export FIRECRAWL_API_KEY="fc-..."
app = FirecrawlApp()


# 2. Define the exact JSON schema you want the AI to return
class PricingPlan(BaseModel):
    plan_name: str = Field(description="The name of the pricing tier or plan")
    price_monthly: Optional[float] = Field(description="Monthly price in USD. Null if free or custom.")
    features: List[str] = Field(description="List of top 3 features included in this plan")


class CompanyPricingSchema(BaseModel):
    company_name: str = Field(description="Name of the company or product")
    pricing_model: str = Field(description="Pricing model type, e.g., SaaS subscription, usage-based, flat-fee")
    plans: List[PricingPlan] = Field(description="Array of all available pricing plans found on the page")


# 3. Run the structured scrape execution
try:
    print("Scraping and extracting structured data...")

    # We will use firecrawl.dev/pricing as our target URL
    result = app.scrape_url(
        url='https://firecrawl.dev',
        params={
            'formats': ['extract'],
            'extract': {
                'schema': CompanyPricingSchema.model_json_schema()
            }
        }
    )

    # 4. Output the structured AI-generated response
    print("\n--- Extracted Data Success ---")
    import json

    print(json.dumps(result['extract'], indent=2))

except Exception as e:
    print(f"An error occurred: {e}")
