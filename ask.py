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
        }
    )

    print("\nRESEARCH\n", result["research_notes"])
    print("\nDRAFT\n", result["draft"])
    print("\nCRITIC\n", result["critique"])
    print("\nFINAL\n", result["final_answer"])


if __name__ == "__main__":
    main()