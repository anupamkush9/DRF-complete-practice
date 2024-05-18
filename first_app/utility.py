
def getLimitOffset(request, default_order="asc"):
    DEFAULT_LIMIT = 10   # Means page_size (sepecifies the no of records on per page)
    limit = -1
    offset = 0
    page = 0
    order = default_order

    if (request is not None and request.GET is not None and ('page_size' in request.GET)):
        try:
            DEFAULT_LIMIT = int(request.GET["page_size"])
        except:
            pass

    if (request is not None and request.GET is not None and ('order' in request.GET) and request.GET["order"] in ["asc","desc","ASC","DESC"]):
        order = request.GET["order"].strip().lower()

    if (request is not None and request.GET is not None and ('limit' in request.GET )):
        try:
            limit = int(request.GET["limit"])
        except Exception as e:
            pass

    if (request is not None and request.GET is not None and ('offset' in request.GET)):
        try:
            offset = int(request.GET["offset"])
        except Exception as e:
            pass
    if (request is not None and request.GET is not None and ('page' in request.GET)):
        try:
            page = int(request.GET["page"])
        except Exception as e:
            pass
    if limit == 0 or limit == -1:
        limit = DEFAULT_LIMIT
    else:
        DEFAULT_LIMIT = limit
    records = page - 1 if (page > 0) else 0
    offset = records * limit
    limit = offset + limit
    if limit == -1:
        limit=10
    return offset, limit, page, DEFAULT_LIMIT, order
