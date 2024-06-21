
def getLimitOffset(request, default_order="desc", page_size=10):
    if (request is not None and request.GET is not None and ('page_size' in request.GET)):
        try:
            page_size = int(request.GET["page_size"])
        except:
            pass

    limit = -1
    offset = 0
    page = 0
    order = default_order

    if (request is not None and request.GET is not None and ('order' in request.GET) and request.GET["order"] in ["asc","desc","ASC","DESC"]):
        order = request.GET["order"].strip().lower()

    if (request is not None and request.GET is not None and ('limit' in request.GET or 'offset' in request.GET or 'page' in request.GET)):
        try:
            limit = int(request.GET["limit"])
        except Exception as e:
            pass
        try:
            offset = int(request.GET["offset"])
        except Exception as e:
            pass
        try:
            page = int(request.GET["page"])
        except Exception as e:
            pass
    if page_size <= 0:
        page_size = 10 
    if limit <= 0:
        limit = page_size
    else:
        page_size = limit
    page = 1 if page <= 0 else page
    records = page - 1 if (page > 0) else 0
    offset = records * limit
    limit = offset + limit
    return offset, limit, page, page_size, order
