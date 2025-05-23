import os
import logging
import datetime
from huggingface_hub import InferenceClient
from app.utils.logger import log

# Configure basic logging for the service
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def log2(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] -> {data}")

# class HuggingFaceService:
#     def __init__(self):
#         self.hf_api_token = os.getenv("HF_API_TOKEN")
#         self.hf_model_id = "Qwen/Qwen2.5-7B-Instruct" # "google/flan-t5-base" # "mistralai/Mistral-7B-Instruct-v0.2" 
#         self.client = None
#         if not self.hf_api_token:
#             logger.warning("HF_API_TOKEN not found in environment variables. Hugging Face API calls will not be made.")
#         elif not self.hf_model_id:
#             logger.warning("HF_MODEL_ID not set. Hugging Face API calls will not be made.")
#         else:
#             try:
#                 self.client = InferenceClient(model=self.hf_model_id, token=self.hf_api_token)
#                 logger.info(f"Hugging Face Inference Client initialized for model: {self.hf_model_id}")
#             except Exception as e:
#                 logger.error(f"ERROR: Failed to initialize Hugging Face Inference Client: {e}")
#                 self.client = None

        # --- Mini-RAG: Your hardcoded SAP Knowledge Base ---
        # self.sap_knowledge_base = {
        #     "idoc_status_51": (
        #         "**SAP iDoc Status 51 (Application Document Not Posted):**\n"
        #         "An iDoc status 51 indicates that the iDoc was received by the SAP system "
        #         "but encountered an error during application posting. This means the data "
        #         "could not be successfully written to the target SAP application module "
        #         "(e.g., FI, SD, MM). Common causes include missing master data (e.g., customer, "
        #         "material not found), incorrect configuration settings, data validation errors, "
        #         "or missing required segments/fields in the iDoc. "
        #         "To reprocess, use transaction `BD87` (iDoc reprocessing). "
        #         "The error message and status details in `WE02`/`WE05` provide further clues. "
        #         "Often, manual correction of the iDoc data or underlying master data is required."
        #     ),
        #     "sales_order_idoc": (
        #         "**SAP iDoc for Sales Orders (ORDERS05/ORDERS0X):**\n"
        #         "Sales orders are typically sent to SAP via iDocs using message type ORDERS. "
        #         "Common iDoc types include ORDERS05 or ORDERS0X variants. "
        #         "Key segments for sales orders include E1EDKA1 (Partner information like Sold-to, Ship-to), "
        #         "E1EDP01 (Item details like material, quantity, unit), "
        #         "E1EDP05 (Pricing conditions), E1EDPT1 (Text segments), etc. "
        #         "Understanding the structure of these segments is crucial for troubleshooting related errors."
        #     ),
        #     "purchase_order_idoc": (
        #         "**SAP iDoc for Purchase Orders (PORDCR1/PORDCRX):**\n"
        #         "Purchase order iDocs often use message type PORDCR1 or similar. "
        #         "They transmit details necessary for creating or changing purchase orders in SAP. "
        #         "Segments like E1EDK01 (PO Header), E1EDP01 (PO Item), E1EDK03 (Dates), and "
        #         "E1EDKA1 (Partner Roles like Vendor) are common. "
        #         "Validation issues related to vendor master data, material master data, or purchasing organizational data are frequent causes of failure."
        #     ),
        #     "idoc_reprocessing": (
        #         "**Reprocessing Failed iDocs (BD87):**\n"
        #         "Transaction code `BD87` is the primary tool for reprocessing failed iDocs in SAP. "
        #         "You can select by iDoc number, status, message type, or time range. "
        #         "Drill down into the iDoc to see the specific error messages and segments. "
        #         "After correcting the cause of the error (e.g., master data, configuration), "
        #         "you can manually reprocess the iDoc from `BD87` to attempt posting again."
        #     ),
        #     "prompt_ideas": [
        #         "idoc_status_analysis",
        #         "idoc_traffic_spike_insight",
        #         "segment_error_focus",
        #         "partner_mismatch_alerts",
        #         "idoc_delay_summary"
        #     ]
        # }

#     def _get_relevant_context(self, query: str) -> str:
#         query_lower = query.lower()
#         context_chunks = []

#         if "idoc" in query_lower or "idocs" in query_lower or "51" in query_lower or "failed" in query_lower or "error" in query_lower:
#             context_chunks.append(self.sap_knowledge_base["idoc_status_51"])
#         if "sales order" in query_lower or "orders0" in query_lower or "va01" in query_lower:
#             context_chunks.append(self.sap_knowledge_base["sales_order_idoc"])
#         if "purchase order" in query_lower or "pordcr" in query_lower or "me21n" in query_lower:
#             context_chunks.append(self.sap_knowledge_base["purchase_order_idoc"])
#         if "reprocess" in query_lower or "bd87" in query_lower:
#             context_chunks.append(self.sap_knowledge_base["idoc_reprocessing"])

#         unique_contexts = list(set(context_chunks))
#         if unique_contexts:
#             return "\n\n".join(unique_contexts)
#         return ""

#     def generate_text(self, prompt: str, include_sap_context: bool = True) -> str:
#         if not self.client:
#             raise Exception("Hugging Face Inference API is not configured.")

#         final_llm_prompt = ""
#         if include_sap_context:
#             relevant_sap_context = self._get_relevant_context(prompt)
#             if relevant_sap_context:
#                 augmented_prompt = (
#                     f"Based on the following SAP documentation, please answer the question. "
#                     f"Prioritize information from the provided documentation:\n\n"
#                     f"{relevant_sap_context}\n\n"
#                     f"Question: {prompt}\n\n"
#                     f"Answer:"
#                 )
#                 logger.info("SAP context successfully added to prompt.")
#                 log("Augmented Prompt created - SAP context successfully added to prompt.")
#             else:
#                 logger.info("No specific SAP context found for the query. Proceeding with original prompt.")
#                 log("No specific SAP context found for the query. Proceeding with original prompt.")
#                 augmented_prompt = prompt
#         else:
#             logger.info("SAP context inclusion skipped as requested.")
#             log.info("SAP context inclusion skipped as requested.")
#             augmented_prompt = prompt

#         # final_llm_prompt = f"<s>[INST] {augmented_prompt} [/INST]"
#         final_llm_prompt = augmented_prompt
#         logger.debug(f"Sending prompt to HF (first 500 chars): {final_llm_prompt[:500]}...")
#         log(f"Sending prompt to HF (first 500 chars): {final_llm_prompt[:500]}...")

#         try:
#             # response = self.client.text_generation(
#             #     final_llm_prompt,
#             #     max_new_tokens=300,
#             #     temperature=0.4,
#             #     stop_sequences=["</s>", "\nUser:", "\nAssistant:", "Question:"]
#             # )
#             response = self.client.conversational(
#                 prompt=final_llm_prompt,
#                 max_new_tokens=300,
#                 temperature=0.4
#             )
            
#             generated_text = str(response).strip()            
#             if generated_text.lower().startswith("answer:"):
#                 generated_text = generated_text[len("answer:"):].strip()
#             if generated_text.lower().startswith("based on the documentation,"):
#                 generated_text = generated_text[len("based on the documentation,"):].strip()
#             logger.info("Text generated successfully from Hugging Face.")
#             return generated_text
#         except Exception as e:
#             logger.error(f"Hugging Face API call failed: {e}", exc_info=True)
#             raise Exception(f"Failed to generate text from Hugging Face: {str(e)}")


# FILE: app/zidoc_api/hf_service.py
import os
import logging
from huggingface_hub import InferenceClient
from app.utils.logger import log

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        self.hf_api_token = os.getenv("HF_API_TOKEN")
        self.hf_model_id = "Qwen/Qwen2.5-7B-Instruct"
        self.client = None

        if not self.hf_api_token:
            logger.warning("HF_API_TOKEN not found in environment variables.")
        else:
            try:
                self.client = InferenceClient(
                    model=self.hf_model_id,
                    provider="together",
                    token=self.hf_api_token
                )
                logger.info(f"Hugging Face Inference Client initialized for model: {self.hf_model_id}")
                log2(f"Hugging Face Inference Client initialized for model: {self.hf_model_id}")
            except Exception as e:
                logger.error(f"ERROR: Failed to initialize Hugging Face Inference Client: {e}")
                log2(f"ERROR: Failed to initialize Hugging Face Inference Client: {e}")
                self.client = None

        # Keep it lean since model is strong
        self.sap_knowledge_base = {
            "idoc_status_51": "iDoc 51 error analysis",
            "sales_order_idoc": "Sales order iDoc issues",
            "purchase_order_idoc": "Purchase order iDoc issues",
            "idoc_reprocessing": "How iDoc reprocessing works (e.g., BD87)",
            "prompt_ideas": [
                "idoc_status_analysis",
                "idoc_traffic_spike_insight",
                "segment_error_focus",
                "partner_mismatch_alerts",
                "idoc_delay_summary"
            ]
        }

    def _get_relevant_context(self, query: str) -> str:
        query_lower = query.lower()
        context_chunks = []

        if any(term in query_lower for term in ["idoc", "51", "failed", "error"]):
            context_chunks.append(self.sap_knowledge_base["idoc_status_51"])
        if any(term in query_lower for term in ["sales order", "orders0", "va01"]):
            context_chunks.append(self.sap_knowledge_base["sales_order_idoc"])
        if any(term in query_lower for term in ["purchase order", "pordcr", "me21n"]):
            context_chunks.append(self.sap_knowledge_base["purchase_order_idoc"])
        if "reprocess" in query_lower or "bd87" in query_lower:
            context_chunks.append(self.sap_knowledge_base["idoc_reprocessing"])
        log2("Tried Getting Relevant Context Chunks")

        return ", ".join(set(context_chunks)) if context_chunks else ""

    def freestyle_text_gen(self, prompt: str) -> str:
        """Freestyle chat wrapper for /hfchat endpoint"""
        if not self.client:
            raise Exception("Hugging Face client not initialized.")

        final_prompt = (
            f"{prompt}\n\nNote: Keep the response brief and relevant. Avoid excessive explanation."
        )

        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}]
            )
            log2("Chat Completions API - Freestyle...")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Freestyle LLM call failed: {e}", exc_info=True)
            raise Exception(f"LLM freestyle inference failed: {str(e)}")

    def generate_inference_text(self, query: str) -> str:
        """ZIDOC analytics-focused inference wrapper"""
        if not self.client:
            raise Exception("Hugging Face client not initialized.")

        topic_string = self._get_relevant_context(query)

        final_prompt = (
            f"Context topics: {topic_string}.\n"
            f"You are an SAP iDoc analyst. Based on the above context and the question below, "
            f"give a concise, clean HTML-formatted insight with no preamble or generic disclaimers.\n"
            f"<b>Question:</b> {query}"
        )

        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": final_prompt}]
            )
            log2("Chat Completions API - iDoc Inference...")
            raw = completion.choices[0].message.content.strip()

            # Basic cleanup for common LLM prefixes
            for unwanted in ["Answer:", "Based on the context,", "Here's the insight:"]:
                if raw.lower().startswith(unwanted.lower()):
                    raw = raw[len(unwanted):].strip()
            return raw

        except Exception as e:
            logger.error(f"Inference LLM call failed: {e}", exc_info=True)
            raise Exception(f"LLM analytics inference failed: {str(e)}")

# Global singleton instance for reuse across endpoints and modules
hf_service = HuggingFaceService()
