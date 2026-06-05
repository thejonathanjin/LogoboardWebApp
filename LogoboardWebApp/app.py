import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sample of Top Brands Data (Name and Logo URL)
# In a production app, this could be a full list of 100
BRANDS = [
    {"name": "Presidential Seal of The United States", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/Seal_of_the_President_of_the_United_States.svg"},
    {"name": "Air Force One", "logo": "https://airportag.com/cdn/shop/products/air-force-one-pin-main.jpg?v=1665580562&width=2048"},
    {"name": "Harvard University", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Harvard_University_coat_of_arms.svg/1280px-Harvard_University_coat_of_arms.svg.png"},
    {"name": "DNC", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/US_Democratic_Party_Logo.svg/500px-US_Democratic_Party_Logo.svg.png"},
    {"name": "NBC", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/NBC_logo.svg/1280px-NBC_logo.svg.png"},
    {"name": "Lifetime", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Logo_Lifetime_2020.svg/1280px-Logo_Lifetime_2020.svg.png"},
    {"name": "Saturday Night Live", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/06/SNL_logo_2015.png"},
    {"name": "Planned Parenthood", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Planned_Parenthood.png"},
    {"name": "Forward Together", "logo": "https://order-site-images-dev.imgix.net/ceb94f03-31be-4593-8b99-5a9a6ebe248e/HRC_LOGO.svg"},
    {"name": "New York Flag", "logo": "https://cdn.britannica.com/14/3014-050-17B84006/flag-New-York-color-uniforms-facings-American-1909.jpg"},
    {"name": "California Flag", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Flag_of_California.svg/1280px-Flag_of_California.svg.png"},
    {"name": "Santa Clara University", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/a/ad/Santa_Clara_U_Seal.svg/1280px-Santa_Clara_U_Seal.svg.png"},
    {"name": "Baskin-Robbins", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Baskin-Robbins_logo.svg/960px-Baskin-Robbins_logo.svg.png"},
    {"name": "Google Vintage", "logo": "https://cdn.logojoy.com/wp-content/uploads/20230801145708/google-logo-1999-600x217.png"},
    {"name": "Art Storefronts", "logo": "https://images.discerningassets.com/image/upload/v1674082181/sjbjwlaemd2xaw3pvtkd.png"},
    {"name": "YouTube", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Logo_of_YouTube_%282015-2017%29.svg/3840px-Logo_of_YouTube_%282015-2017%29.svg.png"},
    {"name": "Yahoo! Vintage", "logo": "https://logos-world.net/wp-content/uploads/2020/10/Yahoo-Logo-2009-2013.png"},
    {"name": "Windows Vintage", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Windows_Logo_%281992-2001%29.svg"},
    {"name": "Apple Vintage", "logo": "https://www.logogenie.com/images/articles/apple-logo-article3.jpg"},
    {"name": "Blockbuster", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Blockbuster_logo.svg/3840px-Blockbuster_logo.svg.png"},
    {"name": "Nintendo", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/SNES_logo.svg/960px-SNES_logo.svg.png"},
    {"name": "America Online", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/America_Online_logo.svg/1280px-America_Online_logo.svg.png"},
    {"name": "AOL Instant Messenger", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5a/AIM_logo.svg"},
    {"name": "Henri Selmer Paris", "logo": "https://upload.wikimedia.org/wikipedia/en/2/2e/Henri_selmer_paris_logo.png"},
    {"name": "PlumpJack Winery", "logo": "https://plumpjackwines.com/cdn/shop/files/PJWine_Spirits-02_4242x.png?v=1668627392"},
    {"name": "Silicon Valley Bank", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Silicon_Valley_Bank_logo%2C_2022.svg/1280px-Silicon_Valley_Bank_logo%2C_2022.svg.png"},
    {"name": "The Obama Campaign", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Obama_logomark.svg/1280px-Obama_logomark.svg.png"},
    {"name": "United Nations", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Logo_of_the_United_Nations.svg"},
    {"name": "X.com", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/X_icon.svg/960px-X_icon.svg.png"},
    {"name": "The Joe Rogan Experience", "logo": "https://upload.wikimedia.org/wikipedia/en/e/e3/The_Joe_Rogan_Experience_logo.png"},
    {"name": "Apple", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"},
    {"name": "Microsoft", "logo": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"},
    {"name": "Google", "logo": "https://download.logo.wine/logo/Google/Google-Logo.wine.png"},
    {"name": "Amazon", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg"},
    {"name": "Blue Origin", "logo": "https://download.logo.wine/logo/Blue_Origin/Blue_Origin-Logo.wine.png"},
    {"name": "NVIDIA", "logo": "https://upload.wikimedia.org/wikipedia/sco/2/21/Nvidia_logo.svg"},
    {"name": "Samsung", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg"},
    {"name": "Walmart", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg"},
    {"name": "Facebook", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Facebook_Logo_2023.png/1280px-Facebook_Logo_2023.png"},
    {"name": "Facebook Live", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Facebook_Live.svg/1280px-Facebook_Live.svg.png"},
    {"name": "Instagram", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/3840px-Instagram_logo_2016.svg.png"},
    {"name": "TikTok", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg"},
    {"name": "YouTube", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg"},
    {"name": "Coca-Cola", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_logo.svg"},
    {"name": "Mercedes-Benz", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/90/Mercedes-Benz_Logo_2010.svg"},
    {"name": "Toyota", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Toyota_EU.svg"},
    {"name": "McDonald's", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/36/McDonald%27s_Golden_Arches.svg"},
    {"name": "Disney", "logo": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney_2012_logo.svg"},
    {"name": "Nike", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Logo_NIKE.svg"},
    {"name": "Tesla", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Tesla_Motors.svg"},
    {"name": "NASA", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/960px-NASA_logo.svg.png"},
    {"name": "Visa", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Visa_2021.svg"},
    {"name": "Netflix", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"},
    {"name": "Oracle", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/50/Oracle_logo.svg"},
    # {"name": "Intel", "logo": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Intel_logo_%282020%29.svg"},
    {"name": "Intel Vintage", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Intel_Inside_Logo_%281991-2006%29.svg"},
    {"name": "IBM", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg"},
    {"name": "Starbucks", "logo": "https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg"},
    {"name": "Adidas", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/20/Adidas_Logo.svg"},

    {"name": "Tesla and Zip2", "logo": "https://www.tesla.com/ns_videos/vin-decoder/tesla-logo.png"},
    {"name": "Boeing", "logo": "https://www.boeing.com/resources/boeingdotcom/boeing_logo.png"},
    {"name": "Ford", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ford_logo_flat.svg/3840px-Ford_logo_flat.svg.png"},
    {"name": "General Motors", "logo": "https://www.gm.com/content/dam/gm/common/gm-logo-2021.svg"},
    {"name": "SpaceX", "logo": "https://www.logo.wine/a/logo/SpaceX/SpaceX-White-Dark-Background-Logo.wine.svg"},
    {"name": "Lockheed Martin", "logo": "https://www.lockheedmartin.com/content/dam/lockheed-martin/eo/eo-logo.png"},
    {"name": "Northrop Grumman", "logo": "https://www.northropgrumman.com/wp-content/themes/ngc/assets/images/logo.svg"},
    {"name": "Raytheon (RTX)", "logo": "https://www.rtx.com/sites/default/files/styles/hero_desktop/public/2023-01/RTX_Logo.png?h=3e2d6b3a&itok=O1eZ2o_l"},
    {"name": "General Dynamics", "logo": "https://www.gd.com/images/GDLogo.svg"},
    {"name": "Rivian", "logo": "https://rivian.com/assets/2022/shared/logo.svg"},
    {"name": "Lucid Motors", "logo": "https://www.lucidmotors.com/app/themes/lucid/dist/images/logo.svg"},
    {"name": "United Launch Alliance (ULA)", "logo": "https://www.ulalaunch.com/images/default-source/default-album/ula-logo.svg"},
    {"name": "Honeywell Aerospace", "logo": "https://aerospace.honeywell.com/content/dam/aerospace/en/images/homepage/honeywell-logo-black.svg"},
    {"name": "Ball Aerospace", "logo": "https://www.ball.com/getmedia/e8e046c8-508b-4a5c-8d19-5777a834947d/Ball-Logo"},
    {"name": "L3Harris Technologies", "logo": "https://www.l3harris.com/sites/default/files/styles/logo_header/public/L3Harris_logo.svg"},
    {"name": "Harley-Davidson", "logo": "https://www.harley-davidson.com/content/dam/hd/images/logo/logo-white.svg"},
    {"name": "Jeep", "logo": "https://www.jeep.com/content/dam/fca-brands/na/jeep/en_us/header/jeep-logo.svg"},
    {"name": "Ram Trucks", "logo": "https://www.ramtrucks.com/content/dam/fca-brands/na/ram/en_us/header/ram-logo.svg"},
    {"name": "Cadillac", "logo": "https://www.cadillac.com/content/dam/cadillac/na/us/com/index/logo/cadillac-logo.svg"},
    {"name": "Sierra Nevada Corporation", "logo": "https://www.sncorp.com/assets/logo.svg"},
    {"name": "Aerojet Rocketdyne", "logo": "https://www.rocket.com/sites/default/files/styles/large/public/AerojetRocketdyneLogo_0.png"},
    {"name": "Tesla Energy", "logo": "https://www.tesla.com/ns_videos/vin-decoder/tesla-logo."},

    {"name": "Fender", "logo": "https://assets.spotlight.fender.com/logos/fender-red-large.jpg"},
    {"name": "Gibson", "logo": "https://images.gibson.com/gibson-logo-black.svg"},
    {"name": "Martin Guitar", "logo": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Martin_guitar_logo.png"},
    {"name": "Taylor Guitars", "logo": "https://www.taylorguitars.com/sites/default/files/styles/hero_image/public/images/logo/Taylor-logo-1000px.png"},
    {"name": "Steinway & Sons", "logo": "https://www.steinway.com/assets/client/images/logo-steinway-black.svg"},
    {"name": "Yamaha", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Yamaha_logo.svg"},
    {"name": "Roland", "logo": "https://www.roland.com/global/common/images/logo_roland.svg"},
    {"name": "Shure", "logo": "https://www.soundandcommunications.com/wp-content/uploads/2020/04/Shure-Logo-759x500-1.jpg"},
    {"name": "Kawai", "logo": "https://www.kawai-global.com/wp-content/themes/kawai-global/images/logo.svg"},
    {"name": "Audio-Technica", "logo": "https://www.soundadviceav.co.uk/wp-content/uploads/2018/11/audio-technica-logo.jpg"},
    {"name": "Paiste", "logo": "https://www.paiste.com/uploads/images/logo.png"},
    {"name": "Beyerdynamic", "logo": "https://global.beyerdynamic.com/media/logo/stores/1/beyerdynamic_logo_2022.svg"},
    {"name": "Jupiter", "logo": "https://jupitermusic.us/sites/jupitermusic/files/2024-03/Jupiter%20Logo.png"},
    {"name": "Ibanez", "logo": "https://static.wikia.nocookie.net/ibanez/images/d/da/Ibanez_guitars_logo.png"},
    {"name": "PRS Guitars", "logo": "https://images.ctfassets.net/74ch1hskxran/14ENltnkuUJoXosmJ329pB/7ba6af212533b46f1782dc4dd4794dc5/brand-prs-paul-reed-smith-guitars.jpg"},
    {"name": "Gretsch", "logo": "https://www.gretschguitars.com/sites/gretschguitars/files/styles/logo_header/public/images/logo/Gretsch_Logo_Black.png"},
    {"name": "Korg", "logo": "https://www.korg.com/common/images/logo.svg"},
    {"name": "Zildjian", "logo": "https://zildjian.com/cdn/shop/files/Zildjian_Logo_Black_e48d39e1-64d5-4c07-9519-c603a1661664_150x.png"},
    {"name": "DW Drums", "logo": "https://www.dwdrums.com/wp-content/themes/dwdrums/images/dw-logo.svg"},
    {"name": "Moog Music", "logo": "https://moogmusic.com/sites/default/files/styles/logo/public/logo/moog-logo.svg"},
    {"name": "Behringer", "logo": "https://www.behringer.com/files/assets/behringer_logo_new.svg"},
    {"name": "Boss", "logo": "https://www.boss.info/global/common/images/logo_boss.svg"},
    {"name": "EV (Electro-Voice)", "logo": "https://products.electrovoice.com/binary/EV_logo_black.png"},
    {"name": "Sennheiser", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/97/Sennheiser_Logo.png"},

    {"name": "Chan Zuckerberg Initiative", "logo": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Chan_Zuckerberg_Initiative.svg"},
    {"name": "Ray Ban", "logo": "https://logoeps.com/wp-content/uploads/2012/10/ray-ban-vector-logo.png"},
    {"name": "Lenovo ThinkPad", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Lenovo_Global_Corporate_Logo.png/1280px-Lenovo_Global_Corporate_Logo.png"},
    {"name": "Sony VAIO", "logo": "https://download.logo.wine/logo/Vaio/Vaio-Logo.wine.png"},
    {"name": "Patagonia", "logo": "https://logos-world.net/wp-content/uploads/2020/05/Patagonia-Emblem.jpg"},
    {"name": "Prada", "logo": "https://logo.com/image-cdn/images/kts928pd/production/5be7f05ad50b4254e440898461e4ad1026a11723-900x592.png?w=1920&q=72&fm=webp"},

    {"name": "nvidia", "logo": "https://logos-world.net/wp-content/uploads/2020/11/Nvidia-Symbol.jpg"},
    {"name": "Stanford University", "logo": "https://www.designyourway.net/blog/wp-content/uploads/2024/04/the-meaning-behind-the-stanford-university-logo.png"},
    {"name": "Denny's", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Denny%27s_Logo_06.2022.svg/3840px-Denny%27s_Logo_06.2022.svg.png"},
    {"name": "Dolby Labs", "logo": "https://cdn.freebiesupply.com/logos/large/2x/dolby-laboratories-logo-png-transparent.png"},
    {"name": "Creative Labs", "logo": "https://img.creative.com/images/corporate/logos/logo_creative_color.png?v=1"},
    {"name": "Sound Blaster", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Sound_Blaster_logo.svg/3840px-Sound_Blaster_logo.svg.png"},

    {"name": "Two-Rock Amplifiers", "logo": "https://cdn.shopify.com/s/files/1/0613/5028/1439/collections/472552b9f7ada477c3d124d5ad89db26.jpg?v=1665180227"},
    {"name": "GQ Magazine", "logo": "https://logos-world.net/wp-content/uploads/2023/04/GQ-Emblem.png"},
    {"name": "G-Shock", "logo": "https://cdn.freebiesupply.com/logos/large/2x/g-shock-casio-logo-black-and-white.png"},
    {"name": "Rolex", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Logo_da_Rolex.png"},

    {"name": "Rickenbacker", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Rickenbacker_logo.svg/1280px-Rickenbacker_logo.svg.png"},
    {"name": "Hofner", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Hofner_logo.png/250px-Hofner_logo.png"},
    {"name": "Juno-106 Programmable Synthesizer", "logo": "https://blog.thea.codes/the-design-of-the-juno-dco/juno-logo.png"},
    {"name": "Fender Stratocaster", "logo": "https://www.muraldecal.com/en/img/guit018-jpg/folder/products-listado-merchanthover/stickers-fender-stratocaster.jpg"},
    {"name": "Ludwig Drums", "logo": "https://upload.wikimedia.org/wikipedia/commons/1/12/Ludwig_logo.png"},
    {"name": "Zildjan", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Zildjian_Logo.svg/1280px-Zildjian_Logo.svg.png"},
    {"name": "Akai Professional", "logo": "https://images.ctfassets.net/74ch1hskxran/2o73Jlwg0zyWHNh4eL1NwD/d02ff597bbc805ad4a431464e2c2f312/brand-akai.jpg"},
    {"name": "Yamaha", "logo": "https://static.vecteezy.com/system/resources/thumbnails/014/414/660/small/yamaha-black-logo-on-transparent-background-free-vector.jpg"},
    {"name": "Crown | Penguin Random House", "logo": "https://prhinternationalsales.com/wp-content/uploads/2017/06/Crown_Pub_Group_PRH_logo_color-2.jpg"},
    {"name": "Apple Podcasts", "logo": "https://logos-world.net/wp-content/uploads/2021/10/Podcast-Emblem.png"},
    {"name": "Spotify", "logo": "https://download.logo.wine/logo/Spotify/Spotify-Logo.wine.png"},
    {"name": "Audible", "logo": "https://download.logo.wine/logo/Audible_(store)/Audible_(store)-Logo.wine.png"},
    {"name": "Air Force One Seal", "logo": "https://plaquesandpatches.com/wp-content/uploads/images/products/products-USAF-Seal.jpg"},
    {"name": "BlackBerry", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/95/Blackberry-logo-vector_c%C3%B3pia.jpg"},
    {"name": "Twitter", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Twitter_2012_logo.svg/3840px-Twitter_2012_logo.svg.png"},
    {"name": "J. Crew", "logo": "https://logos-world.net/wp-content/uploads/2023/12/J-Crew-Emblem.png"},

    {"name": "AVID Pro Tools", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d6/PT2019.svg"},
    {"name": "Dior", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Dior_Logo.svg/1280px-Dior_Logo.svg.png"},
    {"name": "Louis Vuitton", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Louis_Vuitton_logo_and_wordmark.svg/250px-Louis_Vuitton_logo_and_wordmark.svg.png"},
    {"name": "Equipboard", "logo": "https://mma.prnewswire.com/media/2595823/Equipboard_primary_logo_black.jpg?p=facebook"},

    {"name": "Tidal", "logo": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Tidalhifi.jpg"},
    {"name": "Rocnation", "logo": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Roc_Nation_logo.png"},
    {"name": "Rocawear", "logo": "https://cdn.freebiesupply.com/logos/large/2x/rocawear-logo-png-transparent.png"},
    {"name": "D'Usse", "logo": "https://goodspiritsnews.wordpress.com/wp-content/uploads/2019/07/logo-dusse-cognac-300x300.jpg?w=640"},
    {"name": "Telefunken", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/de/Telefunken.svg"}
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    profile_pic = None
    product_pics = []
    selected_logos = []
    user_text = ""
    bg_color = "#ffffff"

    if request.method == 'POST':
        # 1. Handle Profile Photo
        file = request.files.get('profile_photo')
        if file and allowed_file(file.filename):
            filename = secure_filename("profile_" + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_pic = filename

        # 2. Handle Multiple Product Photos (Up to 8)
        products = request.files.getlist('product_photos')
        for p_file in products[:8]:
            if p_file and allowed_file(p_file.filename):
                p_filename = secure_filename("prod_" + p_file.filename)
                p_file.save(os.path.join(app.config['UPLOAD_FOLDER'], p_filename))
                product_pics.append(p_filename)

        # 3. Handle Text and Background Color
        user_text = request.form.get('user_text', '')
        bg_color = request.form.get('bg_color', '#ffffff')

        # 4. Handle Brand Selection
        selected_brand_names = request.form.getlist('brands')
        selected_logos = [b for b in BRANDS if b['name'] in selected_brand_names]

    return render_template('index.html',
                           brands=BRANDS,
                           profile_pic=profile_pic,
                           product_pics=product_pics,
                           selected_logos=selected_logos,
                           user_text=user_text,
                           bg_color=bg_color)

if __name__ == '__main__':
    app.run(debug=True)
