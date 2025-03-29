from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class ConversationEngine:
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

    def generate(self, prompt: str, max_tokens: int = 150) -> str:
        """生成对话响应"""
        inputs = self.tokenizer(
            f"<|user|>\n{prompt}\n<|assistant|>\n",
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9
        )

        return self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[-1]:],
            skip_special_tokens=True
        )