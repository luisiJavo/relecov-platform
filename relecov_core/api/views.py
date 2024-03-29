from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
    api_view,
    action,
    #    parser_classes,
)
from rest_framework import status
from rest_framework.response import Response
from django.http import QueryDict
from relecov_core.api.serializers import (
    CreateSampleSerializer,
    CreateAuthorSerializer,
    CreateGisaidSerializer,
    CreateEnaSerializer,
)

from relecov_core.api.utils.long_table_handling import fetch_long_table_data
from .utils.analysis_handling import process_analysis_data
from relecov_core.api.utils.sample_handling import (
    check_if_sample_exists,
    split_sample_data,
)
from relecov_core.api.utils.bioinfo_metadata_handling import fetch_bioinfo_data

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from relecov_core.models import SampleState


"""
analysis_data = openapi.Parameter(
    "analysis_name",
    openapi.IN_FORM,
    description="Name of the analsys to be performed",
    type=openapi.TYPE_STRING,
)
analysis_file = openapi.Schema(
    "upload_file",
    in_=openapi.IN_BODY,
    type=openapi.TYPE_FILE,
)
"""


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "analysis_authors": openapi.Schema(
                type=openapi.TYPE_STRING, description="Author of the analysis"
            ),
            "author_submitter": openapi.Schema(
                type=openapi.TYPE_STRING, description="Submitter author to GISAID"
            ),
            "authors": openapi.Schema(
                type=openapi.TYPE_STRING, description="Authors involved in the analysis"
            ),
            "experiment_alias": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Experiment alias used for uploading to ENA",
            ),
            "experiment_title": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Experiment title for uploading to ENA",
            ),
            "fastq_r1_md5": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="MD5 for fastq R1 file",
            ),
            "fastq_r2_md5": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="MD5 for fastq R2 file",
            ),
            "gisaid_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Id given by GISAID",
            ),
            "microbiology_lab_sample_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Sample name ID given by the microbiology lab ",
            ),
            "r1_fastq_filepath": openapi.Schema(
                type=openapi.TYPE_STRING, description="Path where fastq R1 is stored"
            ),
            "r2_fastq_filepath": openapi.Schema(
                type=openapi.TYPE_STRING, description="Path where fastq R2 is stored"
            ),
            "sequence_file_R1_fastq": openapi.Schema(
                type=openapi.TYPE_STRING, description="File name of fastq R1"
            ),
            "sequence_file_R2_fastq": openapi.Schema(
                type=openapi.TYPE_STRING, description="File name of fastq R2"
            ),
            "sequencing_sample_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="Project name"
            ),
            "study_alias": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Study alias used for uplading to ENA",
            ),
            "study_id": openapi.Schema(
                type=openapi.TYPE_STRING, description="Study ID for uploading to ENA"
            ),
            "study_title": openapi.Schema(
                type=openapi.TYPE_STRING, description="Study title for uploading to ENA"
            ),
            "study_type": openapi.Schema(
                type=openapi.TYPE_STRING, description="Study type for uploading to ENA"
            ),
            "submitting_lab_sample_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="sample name id given by the submitted lab",
            ),
        },
    ),
    responses={
        201: "Successful create information",
        400: "Bad Request",
        500: "Internal Server Error",
    },
)
@authentication_classes([SessionAuthentication, BasicAuthentication])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_sample_data(request):
    if request.method == "POST":
        data = request.data
        if isinstance(data, QueryDict):
            data = data.dict()
        # check if sample is alrady defined
        if "sequencing_sample_id" not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if check_if_sample_exists(data["sequencing_sample_id"]):
            error = {"ERROR": "sample already defined"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        data["user"] = request.user.pk
        split_data = split_sample_data(data)
        if "ERROR" in split_data:
            return Response(split_data, status=status.HTTP_400_BAD_REQUEST)

        author_serializer = CreateAuthorSerializer(data=split_data["author"])
        if not author_serializer.is_valid():
            return Response(
                author_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if split_data["gisaid"]["gisaid_id"] != "":
            gisaid_serializer = CreateGisaidSerializer(data=split_data["gisaid"])
            if not gisaid_serializer.is_valid():
                return Response(
                    gisaid_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            gisaid_serializer = None
        if split_data["ena"]["biosample_accession_ENA"] != "":
            ena_serializer = CreateEnaSerializer(data=split_data["ena"])
            if not ena_serializer.is_valid():
                return Response(
                    ena_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            ena_serializer = None
        # Store authors, gisaid, ena in ddbb to get the references
        author_serializer.save()
        if gisaid_serializer:
            gisaid_serializer.save()
        if ena_serializer:
            ena_serializer.save()
        split_data["sample"]["author_obj"] = author_serializer
        split_data["sample"]["gisaid_obj"] = gisaid_serializer
        split_data["sample"]["ena_obj"] = ena_serializer
        sample_serializer = CreateSampleSerializer(data=split_data["sample"])
        if not sample_serializer.is_valid():
            return Response(
                sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        sample_serializer.save()
        return Response("Successful upload information", status=status.HTTP_201_CREATED)


y_param = openapi.Parameter("y", "query", openapi.IN_FORM, type=openapi.TYPE_STRING)

"""
@parser_classes(
    (
        FormParser,
        MultiPartParser,
    )
)
@swagger_auto_schema(
    method="post",
    # manual_parameters=[analysis_file],
    request_body=[y_param],
    responses={
        200: "Successful upload information",
        400: "Bad Request",
        500: "Internal Server Error",
    },
)
"""
# @action(detail=True, methods=['post'], parser_classes=(MultiPartParser, ), name='upload-excel', url_path='upload-excel')


@api_view(["POST"])
@action(detail=False, methods=["post"])
def analysis_data(request):
    if request.method == "POST":
        data = request.data
        if isinstance(data, QueryDict):
            data = data.dict()
        if "analysis" not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        fetched_data = process_analysis_data(data)
        if "ERROR" in fetched_data:
            return Response(fetched_data, status=status.HTTP_400_BAD_REQUEST)
        # if "upload_file" in request.FILES:
        #     a_file = request.FILES["analysis_file"]
        #    print(a_file)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def longtable_data(request):
    if request.method == "POST":
        data = request.data
        if isinstance(data, QueryDict):
            data = data.dict()
        stored_data = fetch_long_table_data(data)
        if "ERROR" in stored_data:
            return Response(stored_data, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def bioinfo_metadata_file(request):
    if request.method == "POST":
        data = request.data

    if isinstance(data, QueryDict):
        data = data.dict()
    stored_data = fetch_bioinfo_data(data)

    if "ERROR" in stored_data:
        return Response(stored_data, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST", "PUT"])
# POST=Create; PUT=Update
def update_state(request):
    if request.method == "POST":
        data = request.data

        if isinstance(data, QueryDict):
            data = data.dict()

        data["user"] = request.user.pk
        if SampleState.objects.filter(state=data["state"]).exists():
            data["state"] = SampleState.objects.filter(state=data["state"]).last().pk
        data["sequencing_sample_id"] = data["sample"]
        sample_serializer = CreateSampleSerializer(data=data)
        if not sample_serializer.is_valid():
            return Response(
                sample_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        sample_serializer.save()
        return Response("Successful upload information", status=status.HTTP_201_CREATED)

    if request.method == "PUT":
        data = request.data

        print("PUT")

        if isinstance(data, QueryDict):
            data = data.dict()

    return Response(status=status.HTTP_201_CREATED)
