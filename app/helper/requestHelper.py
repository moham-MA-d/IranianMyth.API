def validate_myth_id(myth_id):
    myth = Myth.query.get(myth_id)
    if not myth:
        return {"error": f"Myth with id {myth_id} not found"}, 404
    return myth
