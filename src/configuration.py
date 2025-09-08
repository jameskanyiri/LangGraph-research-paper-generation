from pydantic import BaseModel, Field


class Configuration(BaseModel):
    template: str = Field(
        default="""
        # Project Research Paper Template

        ## 1. Title Page
        - Project title, authors, affiliations, contact information.

        ## 2. Abstract
        - Concise summary (problem, method, results, significance).
        - Usually 150–250 words.

        ## 3. Introduction
        - Background and motivation.  
        - Problem definition and research gap.  
        - Contributions (bullet list of what’s new).  
        - Paper organization.

        ## 4. Related Work
        - Prior research and approaches.  
        - Comparative strengths and weaknesses.  
        - Positioning of your work in the literature.

        ## 5. Methodology / Approach
        - **Overall framework/architecture**.  
        - **Core components** (broken down into subsections, e.g., models, algorithms, or modules).  
        - **Phases or steps** of the method.  
        - Example: Initialization → Interaction → Refinement.  
        - **Theoretical justification** (if applicable).  

        ## 6. Implementation Details (optional)
        - Datasets, tools, platforms.  
        - Parameter settings, environments, or configurations.  

        ## 7. Experiments
        - **Benchmarks / datasets used**.  
        - **Baselines for comparison**.  
        - **Evaluation metrics**.  
        - **Results**, often structured as:  
        - Task 1 → Evaluation & results.  
        - Task 2 → Evaluation & results.  
        - Error analysis & ablation studies.  

        ## 8. Discussion / Analysis
        - Interpretation of results.  
        - Insights, strengths, limitations.  
        - Comparison with expectations and related work.  

        ## 9. Conclusion
        - Key takeaways.  
        - Broader implications.  
        - Possible applications.

        ## 10. Future Work / Recommendations
        - Improvements.  
        - Open questions.  
        - Directions for extension.  

        ## 11. References
        - Complete citation list in the chosen style (APA, IEEE, ACM, etc.).

        ## 12. Appendices (if needed)
        - Theoretical proofs.  
        - Extended results/tables.  
        - Dataset or experimental details.  
        - Case studies and examples.  

        """,
        description="Document template",
    )
