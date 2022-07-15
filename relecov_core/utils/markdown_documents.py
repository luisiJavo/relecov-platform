from relecov_core.models import MarkdownDocument


def get_all_documents():
    # markdown_documents = MarkdownDocument.objects.all()
    return MarkdownDocument.objects.all()


def get_documents_by_id(document_id):
    return MarkdownDocument.objects.get(pk__iexact=document_id)
