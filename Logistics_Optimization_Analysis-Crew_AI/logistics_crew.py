import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3,
)

# ── Agents ────────────────────────────────────────────────────────────────────

logistics_analyst = Agent(
    role="Logistics Analyst",
    goal=(
        "Research and analyse the current state of logistics operations, "
        "focusing on route efficiency and inventory turnover trends for the "
        "given list of products."
    ),
    backstory=(
        "You are a seasoned logistics analyst with over 10 years of experience "
        "in supply chain management. You specialise in identifying bottlenecks, "
        "evaluating delivery route performance, and measuring inventory turnover "
        "rates across diverse product categories. Your data-driven insights form "
        "the foundation for every strategic decision in the organisation."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

optimization_strategist = Agent(
    role="Optimization Strategist",
    goal=(
        "Develop actionable optimization strategies for delivery routes and "
        "inventory management based on the analyst's findings, tailored to "
        "the specific products provided."
    ),
    backstory=(
        "You are an expert optimization strategist with a strong background in "
        "operations research and logistics engineering. You translate analytical "
        "findings into concrete, prioritised action plans that reduce costs, "
        "improve delivery times, and maximise inventory efficiency. You are known "
        "for producing strategies that are both ambitious and immediately executable."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# ── Task factory (parametrised by product list) ───────────────────────────────

def build_tasks(products: list[str]) -> tuple[Task, Task]:
    products_str = ", ".join(products)

    analysis_task = Task(
        description=(
            f"Conduct a thorough analysis of the current logistics operations "
            f"for the following products: {products_str}.\n\n"
            "Your analysis must cover:\n"
            "1. Current delivery route efficiency — identify common inefficiencies "
            "   such as long last-mile distances, poor load consolidation, or "
            "   suboptimal sequencing.\n"
            "2. Inventory turnover trends — assess how quickly each product moves "
            "   through the supply chain and highlight slow-moving or overstocked items.\n"
            "3. Key pain points and root causes affecting logistics performance.\n\n"
            "Produce a structured report with clear sections for each product "
            "and a summary of the most critical findings."
        ),
        expected_output=(
            "A structured logistics analysis report containing:\n"
            "- Per-product route efficiency assessment\n"
            "- Per-product inventory turnover analysis\n"
            "- Summary of top pain points and root causes"
        ),
        agent=logistics_analyst,
    )

    strategy_task = Task(
        description=(
            f"Using the logistics analysis report provided by the Logistics Analyst, "
            f"develop a comprehensive optimization strategy for the following products: "
            f"{products_str}.\n\n"
            "Your strategy must include:\n"
            "1. Route optimization recommendations — propose specific improvements "
            "   such as dynamic routing algorithms, load consolidation tactics, or "
            "   hub-and-spoke adjustments.\n"
            "2. Inventory management improvements — recommend reorder point adjustments, "
            "   safety stock levels, or demand forecasting enhancements per product.\n"
            "3. Prioritised action plan — rank recommendations by expected impact and "
            "   ease of implementation.\n"
            "4. Expected KPI improvements — estimate gains in delivery time, cost "
            "   reduction, and inventory turnover for each product.\n\n"
            "The strategy should be practical, data-backed, and ready to present "
            "to senior management."
        ),
        expected_output=(
            "A comprehensive optimization strategy document containing:\n"
            "- Route optimization recommendations per product\n"
            "- Inventory management improvements per product\n"
            "- Prioritised action plan with effort/impact ratings\n"
            "- Estimated KPI improvements"
        ),
        agent=optimization_strategist,
        context=[analysis_task],
    )

    return analysis_task, strategy_task


# ── Crew builder ──────────────────────────────────────────────────────────────

def build_crew(products: list[str]) -> Crew:
    analysis_task, strategy_task = build_tasks(products)
    return Crew(
        agents=[logistics_analyst, optimization_strategist],
        tasks=[analysis_task, strategy_task],
        process=Process.sequential,
        verbose=True,
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("   Logistics Optimization Analysis — Crew AI")
    print("=" * 60)

    raw = input(
        "\nEnter the products to optimise (comma-separated):\n> "
    ).strip()

    if not raw:
        print("No products provided. Using default list.")
        products = ["electronics", "perishable goods", "automotive parts"]
    else:
        products = [p.strip() for p in raw.split(",") if p.strip()]

    print(f"\nRunning analysis for: {', '.join(products)}\n")

    crew = build_crew(products)
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("FINAL OPTIMIZATION STRATEGY")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
