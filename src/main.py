import os
import streamlit as st
import pandas as pd
import yaml
from src.services.scenario_service import run_scenario, compare_scenarios

# -------------------------------------------------
# Sample file locations (bundled with project)
# -------------------------------------------------
current_directory = os.getcwd()
SAMPLE_CSV = current_directory+"/src/data/sample_suppliers.csv"
SAMPLE_YAML = current_directory+"/src/domains/supplier_award.yaml"



def main():
    st.set_page_config(layout="wide")
    st.title("Generic Constraint-Based Optimization Engine")

    # -------------------------------------------------
    # Session initialization (first run defaults)
    # -------------------------------------------------
    if "use_sample" not in st.session_state:
        st.session_state.use_sample = True

    # -------------------------------------------------
    # Input mode selection
    # -------------------------------------------------
    st.sidebar.header("Input Configuration")
    mode = st.sidebar.radio(
        "Select input source",
        ["Sample data (recommended)", "Upload files"],
        index=0 if st.session_state.use_sample else 1
    )

    # -------------------------------------------------
    # Input handling
    # -------------------------------------------------
    if mode == "Upload files":
        st.session_state.use_sample = False

        uploaded = st.file_uploader(
            "Upload Supplier Data (CSV)",
            type=["csv"]
        )
        config_file = st.file_uploader(
            "Upload Domain Config (YAML)",
            type=["yaml", "yml"]
        )

        # -------- Upload guidance --------
        with st.expander("Expected CSV Structure (Required Columns)", expanded=False):
            st.markdown("""
| Column Name | Description |
|------------|------------|
| Supplier | Supplier identifier |
| TotalScore | Composite business score (quality, ESG, risk, etc.) |
| UnitCost | Cost per unit |
| Capacity | Maximum supply capacity |
| SOQ | Standard Order Quantity |
| LeadTime | Lead time in days |

**Notes**
- Column names are **case-sensitive**
- `SOQ` and `Capacity` must be > 0
- Missing columns will raise validation errors
""")

        with st.expander("Expected Domain Config (YAML Structure)"):
            st.code("""
parameters:
  demand:
    type: int
    default: 1000
  lambda_cost:
    type: float
    default: 0.3

variables:
  - name: x
    type: integer
    lower: 0
    upper: Capacity // SOQ

objective:
  var: x
  terms:
    - column: TotalScore
      weight: 1.0
    - column: UnitCost
      weight: -0.3

constraints:
  - type: sum_equals
    var: x
    multiplier: SOQ
    value: demand
""", language="yaml")

    else:
        uploaded = SAMPLE_CSV
        config_file = SAMPLE_YAML

        st.info("Using built-in sample supplier dataset and domain configuration")

        # -------- Sample data preview --------
        st.subheader("Sample Supplier Data")
        sample_df = pd.read_csv(SAMPLE_CSV)
        st.dataframe(sample_df, width='stretch')

        with st.expander("How these columns are used"):
            st.markdown("""
- **TotalScore** → Maximized business value
- **UnitCost** → Penalized in objective (cost sensitivity)
- **Capacity** → Upper bound on awards
- **SOQ** → Fixed order lot size
- **LeadTime** → Eligibility constraint
""")

    # -------------------------------------------------
    # Load data if available
    # -------------------------------------------------
    if uploaded and config_file:
        try:
            df = pd.read_csv(uploaded)

            if mode == "Upload files" :
                #config = yaml.safe_load(config_file.getvalue())
                
                config = yaml.load(config_file, Loader=yaml.FullLoader)
                st.subheader("Supplier Data")
                st.dataframe(df, width='stretch')
            else:
                config = yaml.safe_load(open(config_file))
            
             # -------- Sample data preview --------
       

            # ---------------------------------------------
            # Scenario parameters
            # ---------------------------------------------
            st.sidebar.header("Scenario Parameters")
            params = {}

            for p, meta in config["parameters"].items():
                if meta["type"] == "int":
                    params[p] = st.sidebar.number_input(
                        p, min_value=0,value=meta["default"]
                    )
                elif meta["type"] == "float":
                    params[p] = st.sidebar.slider(
                        p, 0.0, 1.0, meta["default"]
                    )

            # ---------------------------------------------
            # Run optimization
            # ---------------------------------------------
            if st.button("Run Optimization"):
                try:
                    result = run_scenario(df, config, params)

                    if 'error' in st.session_state:
                        st.error(f"optimization error occurred: {st.session_state['error']}", icon="⚠️")

                    st.subheader("Award Results")
                    st.dataframe(
                        result["results"],
                        width='stretch'
                    )

                    st.subheader("Explanations")
                    st.json(result["explanations"])

                except ValueError as e:
                    st.error(str(e), icon="⚠️")

            # ---------------------------------------------
            # Scenario comparison
            # ---------------------------------------------
            if st.button("Compare Cost Sensitivity Scenarios"):
                try:
                    scenarios = compare_scenarios(
                        df,
                        config,
                        params,
                        "lambda_cost",
                        [0.0, 0.3, 0.6, 1.0]
                    )
                    if 'error' in st.session_state:
                        st.error(f"optimization error occurred: {st.session_state['error']}", icon="⚠️")
                    st.subheader("Scenario Comparison")
                    st.dataframe(
                        scenarios,
                        width='stretch'
                    )

                except ValueError as e:
                    st.error(str(e), icon="⚠️")

        except Exception as e:
            st.error(f"Failed to load input files: {e}", icon="⚠️")


"""if __name__ == "__main__":
    main()"""
