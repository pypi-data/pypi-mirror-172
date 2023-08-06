import copy


class JSONToGeoJSONConverter:
    def __init__(self):
        self._nodes_geojson_features: list = []
        self._spans_geojson_features: list = []

    def process_package(self, package_data: dict) -> None:
        for network in package_data.get("networks", []):
            self._process_network(network)

    def _process_network(self, network_data: dict) -> None:
        nodes = network_data.pop("nodes", [])
        spans = network_data.pop("spans", [])
        phases = network_data.pop("phases", [])
        organisations = network_data.pop("organisations", [])

        # Dereference `contracts.relatedPhases`
        if "contracts" in network_data and isinstance(network_data["contracts"], list):
            for contract in network_data["contracts"]:
                if "relatedPhases" in contract and isinstance(
                    contract["relatedPhases"], list
                ):
                    contract["relatedPhases"] = [
                        self._dereference_object(phase, phases)
                        for phase in contract["relatedPhases"]
                    ]

        # Convert nodes to features
        for node in nodes:
            self._nodes_geojson_features.append(
                self._convert_node_to_feature(node, network_data, organisations, phases)
            )

        # Convert spans to features
        for span in spans:
            self._spans_geojson_features.append(
                self._convert_span_to_feature(
                    span, network_data, organisations, phases, nodes
                )
            )

    def get_nodes_geojson(self) -> dict:
        return {"type": "FeatureCollection", "features": self._nodes_geojson_features}

    def get_spans_geojson(self) -> dict:
        return {"type": "FeatureCollection", "features": self._spans_geojson_features}

    def _dereference_object(self, ref, list):
        """
        Return from list the object referenced by ref. Otherwise, return ref.
        """

        if "id" in ref:
            for item in list:
                if item.get("id") == ref["id"]:
                    return item

        return ref

    def _convert_node_to_feature(
        self,
        node_data: dict,
        reduced_network_data: dict,
        organisations: list,
        phases: list,
    ) -> dict:

        reduced_node_data = copy.deepcopy(node_data)

        feature = {"type": "Feature", "geometry": reduced_node_data.pop("location")}

        # Dereference organisation references
        for organisationReference in [
            "physicalInfrastructureProvider",
            "networkProvider",
        ]:
            if organisationReference in reduced_node_data:
                reduced_node_data[organisationReference] = self._dereference_object(
                    reduced_node_data[organisationReference], organisations
                )

        # Dereference phase references
        if "phase" in reduced_node_data:
            reduced_node_data["phase"] = self._dereference_object(
                reduced_node_data["phase"], phases
            )

        feature["properties"] = reduced_node_data
        feature["properties"]["network"] = reduced_network_data

        return feature

    def _convert_span_to_feature(
        self,
        span_data: dict,
        reduced_network_data: dict,
        organisations: list,
        phases: list,
        nodes: list,
    ) -> dict:

        reduced_span_data = copy.deepcopy(span_data)

        feature = {"type": "Feature", "geometry": reduced_span_data.pop("route")}

        # Dereference organisation references
        for organisationReference in [
            "physicalInfrastructureProvider",
            "networkProvider",
        ]:
            if organisationReference in reduced_span_data:
                reduced_span_data[organisationReference] = self._dereference_object(
                    reduced_span_data[organisationReference], organisations
                )

        # Dereference phase references
        if "phase" in reduced_span_data:
            reduced_span_data["phase"] = self._dereference_object(
                reduced_span_data["phase"], phases
            )

        # Dereference endpoints
        for endpoint in ["start", "end"]:
            if endpoint in reduced_span_data:
                for node in nodes:
                    if "id" in node and node["id"] == reduced_span_data[endpoint]:
                        reduced_span_data[endpoint] = node

        feature["properties"] = reduced_span_data
        feature["properties"]["network"] = reduced_network_data

        return feature
