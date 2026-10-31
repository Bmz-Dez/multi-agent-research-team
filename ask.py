from src.graph import build_graph


def main():
    question = input("Question: ").strip()
    if not question:
        print("No question entered.")
        return

    app = build_graph()
    result = app.invoke(
        {
            "question": question,
            "research_notes": "",
            "draft": "",
            "critique": "",
            "final_answer": "",
            "approved": False,
            "revision_count": 0,
        }
    )

    print("\n--- RESEARCH NOTES ---")
    print(result.get("research_notes", ""))

    print("\n--- CRITIC EVALUATION ---")
    print(f"Approved: {result.get('approved')}")
    print(f"Feedback: {result.get('critique')}")
    print(f"Revisions: {result.get('revision_count')}")

    print("\n--- FINAL ANSWER ---")
    print(result.get("final_answer", ""))


if __name__ == "__main__":
    main()