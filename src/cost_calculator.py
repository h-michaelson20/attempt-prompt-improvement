class LLMCostCalculator:
    def __init__(self, df):
        # Use exact column names from the Excel file
        self.input_price_col = 'Input $/M'
        self.output_price_col = 'Output $/M'
        
        # Use the second column as the model name
        self.model_column = df.columns[1]
        
        # Create a clean DataFrame with unique indices
        clean_df = df.drop_duplicates(subset=[self.model_column])
        
        # Extract unique LLM models and their pricing
        self.models_data = clean_df.set_index(self.model_column)[
            [self.input_price_col, self.output_price_col]
        ].to_dict('index')
        
        # Print info for debugging
        print(f"Found {len(self.models_data)} unique models")
        print("Models available:", list(self.models_data.keys()))
    
    def calculate_cost(self, model, input_tokens, output_tokens):
        """Calculate total cost for a given model and token counts"""
        if model not in self.models_data:
            raise ValueError(f"Model {model} not found in pricing data")
            
        model_prices = self.models_data[model]
        input_cost = (input_tokens * model_prices[self.input_price_col]) / 1000000
        output_cost = (output_tokens * model_prices[self.output_price_col]) / 1000000
        
        return {
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': input_cost + output_cost
        } 