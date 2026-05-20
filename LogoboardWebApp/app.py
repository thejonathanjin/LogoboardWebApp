import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Top 25 Brands (Name and Logo URL placeholder)
BRANDS = [
    {"name": "Apple", "logo": "https://substackcdn.com/image/fetch/$s_!G1lk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8ed3d547-94ff-48e1-9f20-8c14a7030a02_2000x2000.jpeg"},
    {"name": "Google", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/500px-Google_%22G%22_logo.svg.png"},
    {"name": "Microsoft", "logo": "https://diplo-media.s3.eu-central-1.amazonaws.com/Microsoft-Logo-HD.jpg"},
    {"name": "Amazon", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/1280px-Amazon_logo.svg.png"},
    {"name": "McDonald's", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/McDonald%27s_logo.svg/1280px-McDonald%27s_logo.svg.png"},
    {"name": "Toyota", "logo": "https://1000logos.net/wp-content/uploads/2018/02/Toyota-logo.png"},
    {"name": "Coca-Cola", "logo": "https://brandlogos.net/wp-content/uploads/2014/12/coca-cola_enjoy-logo_brandlogos.net_rnzay.png"},
    {"name": "Mercedes-Benz", "logo": "https://1000logos.net/wp-content/uploads/2018/04/Mercedes-Benz-Logo.png"},
    {"name": "Disney", "logo": "https://d23.com/app/uploads/2015/07/walt-disney-productions-logos-through-the-years-feat-5.png"},
    {"name": "Samsung", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Samsung_old_logo_before_year_2015.svg/1280px-Samsung_old_logo_before_year_2015.svg.png"},
    {"name": "Nike", "logo": "https://media.about.nike.com/image-downloads/cf68f541-fc92-4373-91cb-086ae0fe2f88/002-nike-logos-swoosh-white.jpg"},
    {"name": "Nvidia", "logo": "https://www.nvidia.com/en-us/about-nvidia/legal-info/logo-brand-usage/_jcr_content/root/responsivegrid/nv_container_392921705/nv_container/nv_image.coreimg.100.1070.png/1703060329053/nvidia-logo-vert.png"},
    {"name": "Facebook", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Facebook_Logo_%282019%29.png/500px-Facebook_Logo_%282019%29.png"},
    {"name": "Instagram", "logo": "https://unblast.com/wp-content/uploads/2025/07/instagram-logo-colored.jpg"},
    {"name": "Visa", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Old_Visa_Logo.svg/1280px-Old_Visa_Logo.svg.png"},
    {"name": "Tesla", "logo": "https://download.logo.wine/logo/Tesla%2C_Inc./Tesla%2C_Inc.-Logo.wine.png"},
    {"name": "BMW", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg"},
    {"name": "Louis Vuitton", "logo": "https://1000logos.net/wp-content/uploads/2017/03/Louis-Vuitton-Logo.jpg"},
    {"name": "Hermès", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/Herm%C3%A8s.svg/1280px-Herm%C3%A8s.svg.png"},
    {"name": "Chanel", "logo": "https://download.logo.wine/logo/Chanel/Chanel-Logo.wine.png"},
    {"name": "Walmart", "logo": "https://cdn.mos.cms.futurecdn.net/5StAbRHLA4ZdyzQZVivm2c.jpg"},
    {"name": "Mastercard", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Mastercard-logo.svg/1280px-Mastercard-logo.svg.png"},
    {"name": "Starbucks", "logo": "https://static.vecteezy.com/system/resources/previews/022/636/379/non_2x/starbucks-logo-starbucks-icon-transparent-free-png.png"},
    {"name": "L'Oréal", "logo": "https://crystalpng.com/wp-content/uploads/2024/08/loreal-logo-png-1.png"},
    {"name": "Adobe", "logo": "https://1000logos.net/wp-content/uploads/2021/04/Adobe-logo.png"},
    {"name": "Christian Dior", "logo": "https://cdn.freebiesupply.com/logos/large/2x/christian-dior-logo-png-transparent.png"}
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    profile_pic = None
    product_pics = []
    selected_logos = []
    text_content = ""
    bg_color = "#ffffff"

    if request.method == 'POST':
        # 1. Handle Profile Photo
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic = filename

        # 2. Handle Product Photos (Multiple, up to 8)
        if 'product_photos' in request.files:
            files = request.files.getlist('product_photos')
            for file in files[:8]:  # Limit to 8
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    product_pics.append(filename)

        # 3. Handle Text and Background
        text_content = request.form.get('enlarged_text', '')
        bg_color = request.form.get('mood_color', '#ffffff')

        # 4. Handle Selected Brand Logos
        selected_brand_names = request.form.getlist('brands')
        selected_logos = [b for b in BRANDS if b['name'] in selected_brand_names]

    return render_template('index.html',
                           brands=BRANDS,
                           profile_pic=profile_pic,
                           product_pics=product_pics,
                           selected_logos=selected_logos,
                           text_content=text_content,
                           bg_color=bg_color)

if __name__ == '__main__':
    app.run(debug=True)