import logging
import time
import utilities.console_text as console_text
import utilities.calculate_timing as calculate_timing
from ai.abstract_ai import AbstractAI
from ai.qa_chain import QAChainAI
from runners.runner import Runner
from langchain.text_splitter import TokenTextSplitter

from documents.vector_database import get_database
from shared.selector import get_embedding

class ProviderLookupRunner(Runner):
    def __init__(self):
        pass
        
    def configure(self):
        pass

    def run(self, abstract_ai:QAChainAI):
        
        # Get the query, which can be multiple lines            
        print("Query (Enter twice to run, X to exit):")

        # Cast the AbstractAI to a QAChainAI
        #qa_chain_ai:QAChainAI = abstract_ai

        # Look up all the entries in the school referrals spreadsheet
        # Load the chroma db that contains the school referrals
        embeddings = get_embedding(abstract_ai.configuration.run_locally)
        school_referrals = get_database(embeddings=embeddings, database_name="sts_school_ss")
        providers = get_database(embeddings=embeddings, database_name="sts_providers")

        # TODO: Make this just loop over every student
        referrals_documents = school_referrals.get()
        providers_documents = providers.get()

        # TODO: Ingest and clean all the data.  This should include the following:
        # 1. Normalize the service names
        # 2. Normalize the provider names and contact info
        # Store it in a database and allow querying by service type


        # Combine all of the providers into a single string
        combined_providers = ''
        for document in providers_documents["documents"]:
            combined_providers += document + "\n"

        # Split those combined providers by token count 
        text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=5)

        split_providers = text_splitter.split_text(combined_providers)
        
        #split_providers = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=["xxxxxxxxxxx"]).split_text(combined_providers)
            

        filtered_referral_documents = []
        for document in referrals_documents["documents"]:
            if "Howe" in document:
                filtered_referral_documents.append(document)

        
        #input("Found " + str(len(filtered_documents)) + " entries. Press enter to process...")

        # Loop over each document and run the query
        for document in filtered_referral_documents:
            service_identification_prompt = """Using the following student data, please extract the following information:
            Whether the service requested is in person, or virtual.
            The service required by the student (if the service required by the student is abbreviated, expand the service required into its full name and description).  
            The current provider, if one is specified.
            
            Your output should be a list of services requested (expanded into their full names), and whether those are in person or virtual, and the existing provider (if one is specified)

            Here are some service type definitions for you to use when identifying the service required:            
            OT: Occupational Therapy - A healthcare profession that helps individuals participate in meaningful activities to enhance their independence and well-being.
            SLP: Speech-Language Pathology - A profession that addresses communication and swallowing disorders to improve individuals' abilities to communicate and eat.
            O&M: Orientation and Mobility - A specialized training to help individuals with visual impairments navigate and move safely and independently in their environment.
            VI: Visual Impairment - A condition that affects a person's vision, potentially leading to various degrees of sight loss.
            BIS-BCBA: Board Certified Behavior Analyst - A professional certification for individuals specializing in behavior analysis, particularly in applied behavior analysis (ABA) therapy.
            Psych: Psychology - The scientific study of behavior and mental processes, including emotions, cognition, and motivation.

            Student Data:             
            {student_info}
            
            """

            print("Student info: " + document)

            service_required_result = abstract_ai.query(service_identification_prompt.format(student_info=document))
            console_text.print_blue(service_required_result.result_string)

            if False:
                # Run the query
                lookup_prompt = """I need your help to find providers that offer the following services:
                Required Service: {services}

                Please look through this provider information below, and see if there is one that might provide the service required.  Only return the information of the service provider if the provide the exact service required.
                
                If there is one or more providers that offers the service, give me the name, email, and phone number of the providers that offer the services described above (also please list the other services the provider offers).

                Provider information:
                {providers}
                """

                for split_provider in split_providers:
                    providers_result = abstract_ai.query(lookup_prompt.format(services=service_required_result.result_string, providers=split_provider))
                    console_text.print_green(providers_result.result_string)
                    console_text.print_green(self.get_source_docs_to_print(providers_result.source_documents))            

                # # print the answer
                # console_text.print_green(result.result_string)            
                # source_docs = self.get_source_docs_to_print(result.source_documents)
                # console_text.print_blue("Source documents:\n" + source_docs)

           
            # Time it
            # start_time = time.time()
                    
            # # Run the query
            # result = abstract_ai.query(query)

            # end_time = time.time()

            # # print the answer
            # console_text.print_green(result.result_string)            
            # source_docs = self.get_source_docs_to_print(result.source_documents)
            # console_text.print_blue("Source documents:\n" + source_docs)
            
            # elapsed_time = end_time - start_time

            # logging.debug("Operation took: " + calculate_timing.convert_milliseconds_to_english(elapsed_time * 1000))
