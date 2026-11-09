# نُهال المعرفة للتدريب والتطوير — nuhal.ae

The site is bilingual: Arabic at `/` and English at `/en/` (same page structure and slugs).

موقع ثابت متعدد الصفحات (HTML/CSS/JS) لشركة **Nuhal Almarifa Training & Development L.L.C** في دبي، باللغة العربية واتجاه RTL، ومهيّأ لمحركات البحث (SEO) ومحركات الإجابة بالذكاء الاصطناعي (GEO).

## الصفحات والروابط
| الصفحة | الرابط |
|---|---|
| الرئيسية | `/` |
| عن الشركة | `/about/` |
| البرامج الحكومية (التقويم الكامل) | `/programs/` |
| 7 صفحات مسارات | `/programs/government-leadership/` · `/programs/digital-transformation/` · `/programs/innovation-customer-experience/` · `/programs/data-cybersecurity-risk/` · `/programs/future-skills/` · `/programs/government-ai/` · `/programs/finance-accounting/` |
| الدورات للأفراد والشركات | `/courses/` |
| 6 صفحات دورات | `/courses/management-leadership/` · `/courses/computer-it/` · `/courses/languages/` · `/courses/educational-services/` · `/courses/professional-skills/` · `/courses/kids/` |
| الاعتمادات | `/accreditations/` |
| الفريق | `/team/` |
| الخبرات | `/experience/` |
| تواصل معنا | `/contact/` |
| النسخة الإنجليزية | نفس الصفحات تحت `/en/` مثل `/en/about/` و`/en/programs/government-ai/` |

## ما يتضمنه كل صفحة من SEO
- عنوان `title` فريد (أقل من 60 حرفاً) ووصف `meta description` فريد (أقل من 155 حرفاً) يركّزان على دبي والإمارات.
- رابط `canonical` و`hreflang` (ar-AE) ووسوم Open Graph وTwitter Card بصورة مناسبة لكل صفحة.
- وسم `geo.region` لدبي (AE-DU).
- بيانات منظّمة JSON-LD: `EducationalOrganization` مع ترخيص KHDA، و`BreadcrumbList`، و`FAQPage`، و`Course` مع `CourseInstance` (التاريخ والمدينة) لكل برنامج، و`Service` لصفحات الدورات.
- عنوان H1 واحد فريد، وروابط داخلية بين المسارات والدورات والصفحات.

كل صفحة عربية مرتبطة بنسختها الإنجليزية عبر `hreflang` (ar-AE / en-AE)، وفي أعلى كل صفحة رابط للتبديل بين اللغتين.

ملفات على مستوى الموقع: `sitemap.xml` و`robots.txt` (يسمح لمحركات الذكاء الاصطناعي) و`llms.txt` و`404.html`.

## النشر
لا يحتاج الموقع أي بناء على الخادم: ارفع محتوى المستودع (عدا مجلد `_build`) إلى استضافة الدومين.
- الروابط الأساسية والبيانات المنظّمة مبنية على `https://www.nuhal.ae/`. إذا كان الدومين مختلفاً، غيّر `SITE` في `_build/content.py` وأعد البناء.
- بعد الإطلاق: أضف الموقع إلى Google Search Console وBing Webmaster Tools وأرسل `sitemap.xml`.

## التعديل وإعادة البناء
المحتوى كله في `_build/content.py` (المسارات والدورات) و`_build/build.py` (بقية الصفحات)، وبيانات التقويم في `_build/items.json`.
```bash
pip install pillow
python3 _build/build.py .
```
حالة كل برنامج (متاح / قيد الانعقاد / منعقد) تُحدَّث تلقائياً في المتصفح حسب تاريخ اليوم.

## النماذج وواتساب
- نماذج التسجيل وطلب البرنامج **ترسل الطلب فعلياً** إلى `hala@nuhal.ae` مع نسخة إلى `nuha@nuhal.ae` عبر خدمة FormSubmit المجانية، دون الحاجة إلى خادم.
- **عند أول طلب** تصل رسالة تفعيل من FormSubmit إلى `hala@nuhal.ae`، ويجب الضغط على رابط التفعيل مرة واحدة فقط لتبدأ الطلبات بالوصول.
- إذا فشل الإرسال لأي سبب، يظهر للعميل نص الطلب جاهزاً للنسخ مع عناوين البريد والهاتف.
- لتغيير البريد المستلم: عدّل `FORM_TO` و`FORM_CC` في `_build/build.py` وأعد البناء.
- زر واتساب عائم في كل الصفحات يفتح محادثة مع `+971 55 701 4016` برسالة جاهزة.

## قبل الإطلاق
- **صفحة الفريق** مبنية على الأدوار، وتُضاف الأسماء والصور عند توفرها.
- **ذكر بلدية دبي** في صفحة الخبرات يحتاج موافقة على عرض اسم الجهة.
- **الاعتمادات:** ترخيص KHDA مؤكد، أما بقية بنود الجودة فتحتاج اعتماد الإدارة.
