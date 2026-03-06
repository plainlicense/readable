# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Basic usage of the readable library."""

from readable import Readability


def main() -> None:
    """Main function to demonstrate basic usage."""
    text = """
    In linguistics, the Gunning fog index is a readability test for English writing.
    The index estimates the years of formal education a person needs to understand
    the text on the first reading. For instance, a fog index of 12 requires the
    reading level of a United States high school senior (around 18 years old).
    The test was developed in 1952 by Robert Gunning, an American businessman
    who had been involved in newspaper and textbook publishing.

    The fog index is commonly used to confirm that text can be read easily by the
    intended audience. Texts for a wide audience generally need a fog index less
    than 12. Texts requiring near-universal understanding generally need an index
    less than 8. Average words per sentence and percentage of complex words are
    the two factors used in the formula.

    Readability formulas are often used in education to help select appropriate
    reading materials for students at different grade levels. They are also
    increasingly used in business and government to ensure that documents are
    accessible to the general public. By simplifying language and shortening
    sentences, writers can improve the readability of their work and reach
    a broader audience.
    """

    # Initialize Readability object
    r = Readability(text)

    # 1. Automated Readability Index (ARI)
    ari = r.ari()
    print("--- ARI ---")
    print(f"Score: {ari.score:.2f}")
    print(f"Grade Levels: {ari.grade_levels}")
    print(f"Ages: {ari.ages}")
    print()

    # 2. Flesch Reading Ease
    flesch = r.flesch()
    print("--- Flesch Reading Ease ---")
    print(f"Score: {flesch.score:.2f}")
    print(f"Ease: {flesch.ease}")
    print(f"Grade Levels: {flesch.grade_levels}")
    print()

    # 3. Flesch-Kincaid Grade Level
    fk = r.flesch_kincaid()
    print("--- Flesch-Kincaid Grade Level ---")
    print(f"Score: {fk.score:.2f}")
    print(f"Grade Level: {fk.grade_level}")
    print()

    # 4. Gunning Fog Index
    gf = r.gunning_fog()
    print("--- Gunning Fog ---")
    print(f"Score: {gf.score:.2f}")
    print(f"Grade Level: {gf.grade_level}")
    print()

    # 5. Coleman-Liau Index
    cl = r.coleman_liau()
    print("--- Coleman-Liau ---")
    print(f"Score: {cl.score:.2f}")
    print(f"Grade Level: {cl.grade_level}")
    print()

    # 6. Dale-Chall Readability
    dc = r.dale_chall()
    print("--- Dale-Chall ---")
    print(f"Score: {dc.score:.2f}")
    print(f"Grade Levels: {dc.grade_levels}")
    print()

    # 7. Statistics
    stats = r.statistics()
    print("--- Statistics ---")
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
