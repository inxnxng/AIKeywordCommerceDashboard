# AIKeywordCommerceDashboard

This repository is dedicated to developing a dashboard that utilizes AI to recommend product keywords and facilitates easy uploading of those products.

## Page Structure
1. GPT 3.5 Conversation
2. Keyword - Product Search
3. Product Upload
4. Product List

## Technology Stack

- Frontend: [Streamlit](https://docs.streamlit.io/)
- Backend: Python 3.12
- OpenAI API: GPT-3.5
- External APIs: 도매꾹 API, 네이버 스마트스토어 API

## Project Installation and Execution

1. **Install Prerequisites:**
   - Install Python 3.12.

2. **Set Environment Variables:**
   - Create a `.env` file and set necessary environment variables.

3. **Configure OpenAI API:**
   - Add the OpenAI API key to the `.env` file.

4. **External API Configuration:**
   - Add the Wholesale Search API, Wholesale Detailed Information API, and Naver Smart Store Product Upload API keys to the `.env` file.

5. **Run the Project:**
   - Run the Frontend and Backend simultaneously.

## Usage

1. Engage in a conversation with OpenAI to receive product keyword recommendations.
2. Use the Wholesale Search API to view a dashboard list of products related to the recommended keywords.
3. Select desired products and click the upload button.
4. Utilize the Wholesale Detailed Information API to retrieve information about the selected products, then use the Naver Smart Store Product Upload API to upload the products.