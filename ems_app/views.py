from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MetaData
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import MetaData

@csrf_exempt
def create_metadata(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            value = None
            velocity = None
            flow = None

            # Navigate to the ports and values array
            ports = data.get("ports", [])
            if ports and isinstance(ports[0], list):
                port_data = ports[0]
                for port in port_data:
                    values = port.get("values", [])
                    for v in values:
                        name = v.get("name", "")
                        val = float(v.get("value", 0))  # convert to float

                        # Match the name to corresponding MetaData field
                        if name == "TOTALIZER":
                            value = val
                        elif name == "FLOW RATE":
                            flow = val
                        elif name == "TEMP":
                            velocity = val

            # Ensure at least one value is found
            if value is not None or velocity is not None or flow is not None:
                metadata = MetaData.objects.create(
                    Value=value,
                    Velocity=velocity,
                    Flow=flow
                )

                return JsonResponse({
                    "message": "MetaData created successfully",
                    "id": metadata.id,
                    "timestamp": metadata.timestamp
                }, status=201)
            else:
                return JsonResponse({"error": "Required data not found in input"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        try:
            metadata_list = MetaData.objects.all().order_by('-timestamp')
            data = [
                {
                    "id": meta.id,
                    "Value": meta.Value,
                    "Velocity": meta.Velocity,
                    "Flow": meta.Flow,
                    "timestamp": meta.timestamp
                }
                for meta in metadata_list
            ]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
