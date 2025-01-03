import joblib
import pandas as pd

# Load the trained model

MODEL_PATH = ""

pipeline = joblib.load('C:/Users/zaver/Downloads/Audiometric_Analyzer-mohan-dev/machine_learning/trained_pipeline.pkl')

# need some development here

def predict_age(array):
    # Make a prediction
    print(array)
    single_entry = pd.DataFrame([array], 
                  columns=['Gender_(M=1/F=0)', 'Age_In_Years', '045dB_20', '045dB_30', '045dB_40', '045dB_50', '045dB_12k', '045dB_12.5K', '045dB_13K', '045dB_13.5K', '045dB_14K', 
                           '045dB_14.5K', '045dB_15K', '045dB_15.5K', '045dB_16K', '045dB_16.5K', '045dB_17K', '045dB_17.5K', '045dB_18K', 
                           '040dB_20', '040dB_30', '040dB_40', '040dB_50', '040dB_12k', '040dB_12.5K', '040dB_13K', '040dB_13.5K', 
                           '040dB_14K', '040dB_14.5K', '040dB_15K', '040dB_15.5K', '040dB_16K', '040dB_16.5K', '040dB_17K', 
                           '040dB_17.5K', '040dB_18K', '035dB_20', '035dB_30', '035dB_40', '035dB_50', '035dB_12k', 
                           '035dB_12.5K', '035dB_13K', '035dB_13.5K', '035dB_14K', '035dB_14.5K', '035dB_15K', 
                           '035dB_15.5K', '035dB_16K', '035dB_16.5K', '035dB_17K', '035dB_17.5K', '035dB_18K'])
    
    prediction = pipeline.predict(single_entry)

    # Output the result
    print(f'Predicted class: {prediction[0]}')
    return(int(prediction[0]))


# Prepare a single entry for prediction as a DataFrame
# single_entry = pd.DataFrame([[1, 29, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]], 
#                   columns=['Gender_(M=1/F=0)', '045dB_20', '045dB_30', '045dB_40', '045dB_50', '045dB_12k', '045dB_12.5K', '045dB_13K', '045dB_13.5K', '045dB_14K', 
#                            '045dB_14.5K', '045dB_15K', '045dB_15.5K', '045dB_16K', '045dB_16.5K', '045dB_17K', '045dB_17.5K', '045dB_18K', 
#                            '040dB_20', '040dB_30', '040dB_40', '040dB_50', '040dB_12k', '040dB_12.5K', '040dB_13K', '040dB_13.5K', 
#                            '040dB_14K', '040dB_14.5K', '040dB_15K', '040dB_15.5K', '040dB_16K', '040dB_16.5K', '040dB_17K', 
#                            '040dB_17.5K', '040dB_18K', '035dB_20', '035dB_30', '035dB_40', '035dB_50', '035dB_12k', 
#                            '035dB_12.5K', '035dB_13K', '035dB_13.5K', '035dB_14K', '035dB_14.5K', '035dB_15K', 
#                            '035dB_15.5K', '035dB_16K', '035dB_16.5K', '035dB_17K', '035dB_17.5K', '035dB_18K'])


# print(predict_age([1, 29, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]))