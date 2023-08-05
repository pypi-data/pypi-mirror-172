from typing import List, Optional, Dict
from wepipe.integrate.postprocessor.base_postprocessor import (
    BasePostprocessorConfig,
    BasePostprocessor,
    TextPayload,
)
from wepipe.integrate.postprocessor.inference_aggregator_function import BaseInferenceAggregateFunction
from wepipe.integrate.preprocessor.text_splitter import TextSplitterPayload


class InferenceAggregatorConfig(BasePostprocessorConfig):
    aggregate_function: BaseInferenceAggregateFunction


class InferenceAggregator(BasePostprocessor):
    def postprocess_input(  # type: ignore[override]
        self, input_list: List[TextPayload], config: InferenceAggregatorConfig, **kwargs
    ) -> List[TextPayload]:
        
        aggregated_payloads = self.segregate_payload(input_list)
        postproces_output: List[TextPayload] = []
        for key, payload_list in aggregated_payloads.items():
            postproces_output.extend(
                config.aggregate_function.execute(payload_list)
            )

        return postproces_output

    @staticmethod
    def segregate_payload(
        input_list: List[TextPayload],
    ) -> Dict[str, List[TextPayload]]:
        segregated_payload: Dict[str, List[TextPayload]] = {}

        # segregate payload
        for idx, payload in enumerate(input_list):
            splitter_data: Optional[TextSplitterPayload] = (
                payload.raw.get("splitter", None) if payload.raw else None
            )
            doc_id = splitter_data.document_id if splitter_data else str(idx)
            if doc_id not in segregated_payload:
                segregated_payload[doc_id] = []
            segregated_payload[doc_id].append(payload)

        # sort based on chunk id
        for doc_id, payloads in segregated_payload.items():
            if (
                len(payloads) > 0
                and payloads[0].raw
                and payloads[0].raw.get("splitter", None)
            ):
                payloads.sort(key=lambda x: x.raw["splitter"].chunk_id)

        return segregated_payload
