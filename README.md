## Chat-Pandas
Chat-Pandas is a tool that allows you to interact with your data in a natural language interface. By using Chat-Pandas, you can ask questions about your data, and the tool will provide you with relevant information.

Also, Chat-Pandas has a frontend by streamlit that allows you to interact with your data in a more intuitive way.

### diary
- 2024-12-9 The first version of Chat-Pandas has been released. In this version, we have implemented the basic functionality of Chat-Pandas, including the ability to query data from a single dataframe. For the frontend, I have implemented a simple interface using __streamlit__. This version only allows you to do the change of the dataframe itself. In the later future, I would like to add the support of data-fitting with sklearn and data visualization with seaborn.

### login
The project can be run locally. If you want to use it in a cloud environment, you need to change the login method. For local running, you can easily login with the username "admin" and password "123456".

### configs
- API Key: Your key for OpenAI
- Model: The model you want to use, me myself recommend the model **gpt-4o-mini**, which has a good balance between speed, accuracy, and cost.
- Base URL: The base URL of the OpenAI API. If you are using a proxy, you can set it to the proxy URL. Remember the URL often ends with /v1, like "https://api.openai.com/v1"
- Max Retries: The maximum number of retries when the API returns an error.
- Use Key: This is a function in the test version, and may be removed in the future. When it is set to False, the answer will be chosen from the fixed pool instead of the OpenAI API.
- Use Rationale: When set to True, the tool will provide a rationale for the answer. By using rationale in generating, the answer generated by the model may be more accurate, by the cost of more time and more tokens.
- Need Dataframe Header: When set to True, the tool will provide the header of the dataframe. By using the header in generating, the model can have a more accurate insight of your dataframe, by the cost of more time and more tokens.





