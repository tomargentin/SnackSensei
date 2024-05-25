import argparse
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
import configparser

class Summarizer:
    def __init__(self, api_key, model_name, pdf_path):
        self.api_key = api_key
        self.model_name = model_name
        self.pdf_path = pdf_path

    def summarize_pdf(self):
        llm = ChatGroq(temperature=0, model_name=self.model_name, api_key=self.api_key)
        loader = PyPDFLoader(self.pdf_path)
        pages = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="stuff")
        response = chain.run(pages)
        return response

def main():

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Summarize a PDF document")

    # Add an argument for the PDF file path
    parser.add_argument("pdf_path", help="Path to the PDF file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the config file
    config.read('config.ini')

    # Get the API key from the config file
    api_key = config['GROQ']['API_KEY']

    # Initialize the Summarizer class
    summarizer = Summarizer(api_key, model_name="mixtral-8x7b-32768", pdf_path=args.pdf_path)

    # Summarize the PDF
    summary = summarizer.summarize_pdf()
    print(summary)

if __name__ == "__main__":
    main()
