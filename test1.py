def image_stats_from_image(I):
    pre_probs = pdf(hist(I))
    pre_error = ssd(pre_probs, ben())

    M = dct(I)
    dct_probs = pdf(hist(M))
    dct_error = ssd(dct_probs, ben())
    
    stats = { 
        "width": I.shape[1],
        "height": I.shape[0],
        "analysis": {
            "pre": {
                "probs": pre_probs,
                "error": pre_error
            }, 
            "dct": {
                "probs": dct_probs,
                "error": dct_error
            }
        }
    }

    return stats

# ----

I = read('IMG_0026.jpeg')
M = dct(I)

h,w = M.shape 
delta = 500

while w >= 8:
    h,w = M.shape
    
    # print progress
    print(f"current width: {w}", end='\r')
    
    stats = image_stats_from_image(M)
    error = stats["analysis"]["dct"]["error"]

    plt.plot(w, error, 'o', color='blue')
    M = cv2.resize(M, (h - delta, w - delta), interpolation=cv2.INTER_AREA)


