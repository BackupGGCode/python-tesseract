[![](http://python-tesseract.googlecode.com/files/sf_coffee_small.jpg)](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)     [If you find python-tesseract useful, please consider ](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USKD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)**_[buying me a coffee.](https://www.paypal.com/cgi-bin/webscr?cmd=_cart&business=VD2Y4PZSK7T86&lc=HK&item_name=To%20support%20the%20development%20of%20python%2dtesseract&amount=5%2e00&currency_code=USKD&button_subtype=products&add=1&bn=PP%2dShopCartBF%3abtn_cart_LG%2egif%3aNonHosted)_**
# V0.9-0.3 #
additional newly wrapped include file:
```
%include "capi.h"
```
all wrapped except
```
TESS_API int   TESS_CALL TessBaseAPIInit;
TESS_API void  TESS_CALL TessBaseAPISetFillLatticeFunc;
```

# V0.9 #

This version wraps all the methods/functions included in
```
%include "pix.h"
%include "publictypes.h"
%include "thresholder.h"
%include "pageiterator.h"
%include "ltrresultiterator.h"
%include "resultiterator.h"
```

and most of the methods/functions included  in
**```
%include "baseapi.h"
```
> except:
```
  typedef int (Dict::*DictFunc)(void* void_dawg_args,
                              UNICHAR_ID unichar_id, bool word_end) const;
  typedef double (Dict::*ProbabilityInContextFunc);

  void SetThresholder(ImageThresholder* thresholder)

  void SetDictFunc(DictFunc f);
  void SetProbabilityInContextFunc(ProbabilityInContextFunc f);
  void SetFillLatticeFunc(FillLatticeFunc f);
```**

~~%include "allheaders.h"~~

~~except:~~

~~LEPT\_DLL extern void setPixMemoryManager;~~