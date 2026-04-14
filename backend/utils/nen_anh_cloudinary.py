def nen_anh_cloudinary_url(url_goc):
    if not url_goc or "cloudinary.com" not in url_goc:
        return url_goc
    
    bua_chu = "upload/q_auto,f_auto,c_scale,w_400"
    
    link_nen = url_goc.replace("/upload/", f"/{bua_chu}/")
    return link_nen