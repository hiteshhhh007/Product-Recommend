import sqlite3
import os

# This script initializes the SQLite database and populates it with product data.
# Run this script once from the `backend` directory before starting the Flask server.

DATABASE_FILE = 'database.db'

# Product data converted from the original TypeScript file
# Replace the existing PRODUCTS_DATA list in your init_db.py with this one.

PRODUCTS_DATA = [
  { "id": 1, "name": 'AeroGlide Drone', "category": 'Electronics', "price": 499.99, "imageUrl": 'https://picsum.photos/seed/drone/400/300', "description": 'High-performance drone with 4K camera and 30-minute flight time.' },
  { "id": 2, "name": 'Quantum VR Headset', "category": 'Electronics', "price": 349.50, "imageUrl": 'https://picsum.photos/seed/vrheadset/400/300', "description": 'Immersive virtual reality experience with high-resolution displays.' },
  { "id": 3, "name": 'SonicWave Earbuds', "category": 'Electronics', "price": 129.00, "imageUrl": 'https://picsum.photos/seed/earbuds/400/300', "description": 'Noise-cancelling wireless earbuds with superior sound quality.' },
  { "id": 10, "name": 'Nebula Smart Projector', "category": 'Electronics', "price": 699.00, "imageUrl": 'https://picsum.photos/seed/projector/400/300', "description": 'Portable 1080p projector with built-in speakers and smart TV capabilities.' },
  { "id": 11, "name": 'Chronos Smartwatch', "category": 'Electronics', "price": 249.99, "imageUrl": 'https://picsum.photos/seed/smartwatch/400/300', "description": 'Track your fitness, notifications, and more with this sleek smartwatch.' },
  { "id": 23, "name": 'GigaPower Portable Charger', "category": 'Electronics', "price": 59.99, "imageUrl": 'https://picsum.photos/seed/powerbank/400/300', "description": '20,000mAh portable charger with fast-charging capabilities for all your devices.' },
  { "id": 24, "name": 'StealthPro Mechanical Keyboard', "category": 'Electronics', "price": 159.99, "imageUrl": 'https://picsum.photos/seed/keyboard/400/300', "description": 'RGB mechanical keyboard with customizable keys and tactile feedback.' },
  { "id": 25, "name": 'CrystalClear 4K Monitor', "category": 'Electronics', "price": 450.00, "imageUrl": 'https://picsum.photos/seed/monitor/400/300', "description": '27-inch 4K UHD monitor with vibrant colors and ultra-thin bezels.' },
  { "id": 26, "name": 'SoundSurge Bluetooth Speaker', "category": 'Electronics', "price": 89.99, "imageUrl": 'https://picsum.photos/seed/speaker/400/300', "description": 'Waterproof portable speaker with 360-degree sound and 12-hour battery life.' },
  { "id": 27, "name": 'ProCam DSLR Camera', "category": 'Electronics', "price": 899.00, "imageUrl": 'https://picsum.photos/seed/camera/400/300', "description": 'Professional DSLR camera with a 24MP sensor and interchangeable lenses.' },
  { "id": 4, "name": 'ErgoComfort Chair', "category": 'Home & Kitchen', "price": 275.00, "imageUrl": 'https://picsum.photos/seed/chair/400/300', "description": 'Ergonomic office chair designed for maximum comfort and support.' },
  { "id": 5, "name": 'SmartBrew Coffee Maker', "category": 'Home & Kitchen', "price": 89.99, "imageUrl": 'https://picsum.photos/seed/coffeemaker/400/300', "description": 'Wi-Fi enabled coffee maker that brews the perfect cup every time.' },
  { "id": 9, "name": 'CulinaryMaster Knife Set', "category": 'Home & Kitchen', "price": 199.99, "imageUrl": 'https://picsum.photos/seed/knifeset/400/300', "description": 'Professional-grade chef knives for precision cutting and slicing.' },
  { "id": 12, "name": 'Aura LED Desk Lamp', "category": 'Home & Kitchen', "price": 79.99, "imageUrl": 'https://picsum.photos/seed/desklamp/400/300', "description": 'Modern desk lamp with adjustable brightness and color temperature.' },
  { "id": 13, "name": 'PureFlow Air Purifier', "category": 'Home & Kitchen', "price": 189.50, "imageUrl": 'https://picsum.photos/seed/airpurifier/400/300', "description": 'HEPA filter air purifier that removes 99.97% of airborne particles.' },
  { "id": 28, "name": 'RoboVaccum V2', "category": 'Home & Kitchen', "price": 399.00, "imageUrl": 'https://picsum.photos/seed/robovacuum/400/300', "description": 'Smart robotic vacuum with mapping technology and self-emptying base.' },
  { "id": 29, "name": 'InstaFry Air Fryer', "category": 'Home & Kitchen', "price": 119.99, "imageUrl": 'https://picsum.photos/seed/airfryer/400/300', "description": '8-quart air fryer for crispy, healthy meals with less oil.' },
  { "id": 30, "name": 'HydroBlend Pro Blender', "category": 'Home & Kitchen', "price": 149.00, "imageUrl": 'https://picsum.photos/seed/blender/400/300', "description": 'High-speed blender for smoothies, soups, and sauces with a 1500W motor.' },
  { "id": 31, "name": 'CozyNights Weighted Blanket', "category": 'Home & Kitchen', "price": 79.99, "imageUrl": 'https://picsum.photos/seed/blanket/400/300', "description": '15lb weighted blanket for a calming and restful sleep experience.' },
  { "id": 32, "name": 'EverGreen Smart Garden', "category": 'Home & Kitchen', "price": 99.50, "imageUrl": 'https://picsum.photos/seed/indoorgarden/400/300', "description": 'Indoor hydroponic garden to grow fresh herbs and vegetables year-round.' },
  { "id": 6, "name": 'HydroPure Water Bottle', "category": 'Sports & Outdoors', "price": 35.00, "imageUrl": 'https://picsum.photos/seed/waterbottle/400/300', "description": 'Insulated stainless steel water bottle that keeps drinks cold for 24 hours.' },
  { "id": 7, "name": 'TerraFirm Hiking Boots', "category": 'Sports & Outdoors', "price": 150.00, "imageUrl": 'https://picsum.photos/seed/hikingboots/400/300', "description": 'Durable and waterproof boots for all your hiking adventures.' },
  { "id": 8, "name": 'FlexFit Yoga Mat', "category": 'Sports & Outdoors', "price": 45.00, "imageUrl": 'https://picsum.photos/seed/yogamat/400/300', "description": 'Eco-friendly, non-slip yoga mat for a perfect practice.' },
  { "id": 14, "name": 'Trailblazer Camping Tent', "category": 'Sports & Outdoors', "price": 220.00, "imageUrl": 'https://picsum.photos/seed/tent/400/300', "description": 'Spacious 4-person tent designed for easy setup and weather resistance.' },
  { "id": 33, "name": 'SpeedFlex Jump Rope', "category": 'Sports & Outdoors', "price": 25.00, "imageUrl": 'https://picsum.photos/seed/jumprope/400/300', "description": 'Adjustable speed jump rope with ball bearings for a smooth workout.' },
  { "id": 34, "name": 'PowerGrip Dumbbell Set', "category": 'Sports & Outdoors', "price": 180.00, "imageUrl": 'https://picsum.photos/seed/dumbbells/400/300', "description": 'Adjustable dumbbell set from 5 to 52.5 lbs for a versatile home gym.' },
  { "id": 35, "name": 'AeroCross Mountain Bike', "category": 'Sports & Outdoors', "price": 750.00, "imageUrl": 'https://picsum.photos/seed/mountainbike/400/300', "description": 'Lightweight aluminum frame mountain bike with 21 speeds and disc brakes.' },
  { "id": 36, "name": 'SummitPro Backpack', "category": 'Sports & Outdoors', "price": 120.00, "imageUrl": 'https://picsum.photos/seed/hikingbackpack/400/300', "description": '50L hiking backpack with ergonomic support and multiple compartments.' },
  { "id": 37, "name": 'GlideFin Kayak', "category": 'Sports & Outdoors', "price": 450.00, "imageUrl": 'https://picsum.photos/seed/kayak/400/300', "description": '10-foot sit-on-top recreational kayak with paddle included.' },
  { "id": 38, "name": 'FireLight Headlamp', "category": 'Sports & Outdoors', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/headlamp/400/300', "description": 'Ultra-bright LED headlamp with 5 modes and rechargeable battery.' },
  { "id": 15, "name": 'The Last Algorithm', "category": 'Books', "price": 19.99, "imageUrl": 'https://picsum.photos/seed/bookscifi/400/300', "description": 'A thrilling science-fiction novel about the dawn of artificial superintelligence.' },
  { "id": 16, "name": 'Echoes of Nebula', "category": 'Books', "price": 24.50, "imageUrl": 'https://picsum.photos/seed/bookfantasy/400/300', "description": 'A high-fantasy epic about a forgotten magic and a looming war.' },
  { "id": 17, "name": 'Culinary Journeys', "category": 'Books', "price": 35.00, "imageUrl": 'https://picsum.photos/seed/cookbook/400/300', "description": 'A beautifully illustrated cookbook featuring recipes from around the world.' },
  { "id": 39, "name": 'The Silicon Mind', "category": 'Books', "price": 22.00, "imageUrl": 'https://picsum.photos/seed/booktech/400/300', "description": 'A non-fiction exploration of the future of AI and human consciousness.' },
  { "id": 40, "name": 'Gardens of the Moon', "category": 'Books', "price": 18.99, "imageUrl": 'https://picsum.photos/seed/bookepic/400/300', "description": 'An epic fantasy novel of empires, assassins, and ancient gods.' },
  { "id": 41, "name": 'Atomic Habits', "category": 'Books', "price": 16.99, "imageUrl": 'https://picsum.photos/seed/bookselfhelp/400/300', "description": 'An easy & proven way to build good habits & break bad ones.' },
  { "id": 42, "name": 'The Midnight Library', "category": 'Books', "price": 15.50, "imageUrl": 'https://picsum.photos/seed/bookfiction/400/300', "description": 'A novel about all the choices that go into a life well-lived.' },
  { "id": 43, "name": 'Sapiens: A Brief History of Humankind', "category": 'Books', "price": 25.00, "imageUrl": 'https://picsum.photos/seed/bookhistory/400/300', "description": 'A groundbreaking narrative of humanity’s creation and evolution.' },
  { "id": 44, "name": 'Project Hail Mary', "category": 'Books', "price": 21.00, "imageUrl": 'https://picsum.photos/seed/bookastronaut/400/300', "description": 'A lone astronaut must save the earth from disaster in this sci-fi thriller.' },
  { "id": 45, "name": 'The Hill We Climb', "category": 'Books', "price": 12.99, "imageUrl": 'https://picsum.photos/seed/bookpoetry/400/300', "description": 'An inaugural poem for the country by Amanda Gorman.' },
  { "id": 18, "name": 'Urban Voyager Jacket', "category": 'Clothing, Shoes & Jewelry', "price": 179.99, "imageUrl": 'https://picsum.photos/seed/jacket/400/300', "description": 'A stylish and waterproof jacket perfect for city life and travel.' },
  { "id": 19, "name": 'All-Weather Running Shoes', "category": 'Clothing, Shoes & Jewelry', "price": 129.50, "imageUrl": 'https://picsum.photos/seed/runningshoes/400/300', "description": 'Lightweight, responsive running shoes with excellent grip for any condition.' },
  { "id": 46, "name": 'Classic Leather Belt', "category": 'Clothing, Shoes & Jewelry', "price": 45.00, "imageUrl": 'https://picsum.photos/seed/leatherbelt/400/300', "description": 'Genuine leather belt with a timeless design and stainless steel buckle.' },
  { "id": 47, "name": 'Merino Wool Socks (3-Pack)', "category": 'Clothing, Shoes & Jewelry', "price": 28.00, "imageUrl": 'https://picsum.photos/seed/woolsocks/400/300', "description": 'Soft, breathable, and odor-resistant socks for all-day comfort.' },
  { "id": 48, "name": 'Diamond Stud Earrings', "category": 'Clothing, Shoes & Jewelry', "price": 299.00, "imageUrl": 'https://picsum.photos/seed/diamondearrings/400/300', "description": 'Elegant 1/4 carat diamond stud earrings set in 14k white gold.' },
  { "id": 49, "name": 'Performance Polo Shirt', "category": 'Clothing, Shoes & Jewelry', "price": 55.00, "imageUrl": 'https://picsum.photos/seed/poloshirt/400/300', "description": 'Moisture-wicking polo shirt with UV protection for sport or casual wear.' },
  { "id": 50, "name": 'Stretch Denim Jeans', "category": 'Clothing, Shoes & Jewelry', "price": 89.00, "imageUrl": 'https://picsum.photos/seed/denimjeans/400/300', "description": 'Modern slim-fit jeans with stretch fabric for maximum comfort.' },
  { "id": 51, "name": 'Canvas Slip-On Sneakers', "category": 'Clothing, Shoes & Jewelry', "price": 65.00, "imageUrl": 'https://picsum.photos/seed/canvassneakers/400/300', "description": 'Comfortable and stylish slip-on sneakers for everyday wear.' },
  { "id": 52, "name": 'Silk Necktie', "category": 'Clothing, Shoes & Jewelry', "price": 39.99, "imageUrl": 'https://picsum.photos/seed/silktie/400/300', "description": 'Handmade 100% silk tie with a classic pattern.' },
  { "id": 53, "name": 'Polarized Aviator Sunglasses', "category": 'Clothing, Shoes & Jewelry', "price": 150.00, "imageUrl": 'https://picsum.photos/seed/sunglasses/400/300', "description": 'Classic aviator sunglasses with polarized lenses to reduce glare.' },
  { "id": 20, "name": 'Starship Explorer LEGO Set', "category": 'Toys & Games', "price": 99.99, "imageUrl": 'https://picsum.photos/seed/legospaceship/400/300', "description": 'Build your own interstellar cruiser with this 1,200-piece creative set.' },
  { "id": 21, "name": 'The Crystal Labyrinth', "category": 'Toys & Games', "price": 49.99, "imageUrl": 'https://picsum.photos/seed/boardgame/400/300', "description": 'A strategic board game of shifting mazes and treasure hunting for 2-4 players.' },
  { "id": 54, "name": 'Remote Control Stunt Car', "category": 'Toys & Games', "price": 39.99, "imageUrl": 'https://picsum.photos/seed/rccar/400/300', "description": 'A fast and durable RC car that can perform 360-degree flips and tricks.' },
  { "id": 55, "name": '1000-Piece Jigsaw Puzzle', "category": 'Toys & Games', "price": 22.50, "imageUrl": 'https://picsum.photos/seed/jigsawpuzzle/400/300', "description": 'A challenging and beautiful jigsaw puzzle featuring a stunning landscape.' },
  { "id": 56, "name": 'MagnaBuilder Magnetic Tiles', "category": 'Toys & Games', "price": 69.99, "imageUrl": 'https://picsum.photos/seed/magnetictiles/400/300', "description": 'A 100-piece set of magnetic building tiles for creative, open-ended play.' },
  { "id": 57, "name": 'Deluxe Watercolor Paint Set', "category": 'Toys & Games', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/watercolorpaint/400/300', "description": 'A 48-color watercolor set with brushes, paper, and a carrying case.' },
  { "id": 58, "name": 'Plush Triceratops Stuffed Animal', "category": 'Toys & Games', "price": 24.99, "imageUrl": 'https://picsum.photos/seed/dinosaurplush/400/300', "description": 'A super-soft and cuddly 15-inch triceratops plush toy.' },
  { "id": 59, "name": 'CodeBot Programming Robot', "category": 'Toys & Games', "price": 119.00, "imageUrl": 'https://picsum.photos/seed/programmingrobot/400/300', "description": 'An educational robot that teaches kids the basics of coding through fun challenges.' },
  { "id": 60, "name": 'Foam Dart Blaster (2-Pack)', "category": 'Toys & Games', "price": 34.99, "imageUrl": 'https://picsum.photos/seed/toygun/400/300', "description": 'A set of two foam dart blasters for exciting indoor and outdoor battles.' },
  { "id": 61, "name": 'Settlers of Catan', "category": 'Toys & Games', "price": 44.00, "imageUrl": 'https://picsum.photos/seed/catanboardgame/400/300', "description": 'The incredibly popular strategy board game of trading, building, and settling.' },
  { "id": 22, "name": 'Revitalize Facial Serum', "category": 'Beauty & Personal Care', "price": 55.00, "imageUrl": 'https://picsum.photos/seed/facialserum/400/300', "description": 'A hydrating and anti-aging serum with Vitamin C and Hyaluronic Acid.' },
  { "id": 62, "name": 'HydroSonic Electric Toothbrush', "category": 'Beauty & Personal Care', "price": 89.99, "imageUrl": 'https://picsum.photos/seed/electrictoothbrush/400/300', "description": 'An electric toothbrush with 5 modes and 40,000 vibrations per minute.' },
  { "id": 63, "name": 'Natural Clay Face Mask', "category": 'Beauty & Personal Care', "price": 24.50, "imageUrl": 'https://picsum.photos/seed/facemask/400/300', "description": 'A detoxifying clay mask to purify pores and leave skin feeling smooth.' },
  { "id": 64, "name": 'Argan Oil Shampoo & Conditioner Set', "category": 'Beauty & Personal Care', "price": 32.00, "imageUrl": 'https://picsum.photos/seed/shampoobottle/400/300', "description": 'A sulfate-free shampoo and conditioner set to nourish and hydrate hair.' },
  { "id": 65, "name": 'Precision Electric Shaver', "category": 'Beauty & Personal Care', "price": 75.00, "imageUrl": 'https://picsum.photos/seed/electricshaver/400/300', "description": 'A waterproof electric shaver for a close, comfortable shave, wet or dry.' },
  { "id": 66, "name": 'Daily Moisturizing Body Lotion', "category": 'Beauty & Personal Care', "price": 14.99, "imageUrl": 'https://picsum.photos/seed/lotionbottle/400/300', "description": 'A fragrance-free body lotion for all-day hydration without a greasy feel.' },
  { "id": 67, "name": 'Mineral Sunscreen SPF 50', "category": 'Beauty & Personal Care', "price": 18.00, "imageUrl": 'https://picsum.photos/seed/sunscreen/400/300', "description": 'A broad-spectrum mineral sunscreen that is gentle on sensitive skin.' },
  { "id": 68, "name": 'Luxury Bath Bomb Set', "category": 'Beauty & Personal Care', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/bathbomb/400/300', "description": 'A set of 12 handcrafted bath bombs with essential oils for a spa-like experience.' },
  { "id": 69, "name": 'Professional Hair Dryer', "category": 'Beauty & Personal Care', "price": 125.00, "imageUrl": 'https://picsum.photos/seed/hairdryer/400/300', "description": 'An ionic hair dryer that reduces frizz and drying time.' },
  { "id": 70, "name": 'Manicure & Pedicure Kit', "category": 'Beauty & Personal Care', "price": 21.99, "imageUrl": 'https://picsum.photos/seed/manicurekit/400/300', "description": 'A 12-piece stainless steel nail care kit in a stylish leather case.' },
  { "id": 71, "name": 'Smart Digital Scale', "category": 'Health & Household', "price": 49.99, "imageUrl": 'https://picsum.photos/seed/digitalscale/400/300', "description": 'A body fat scale that syncs with your phone to track 13 key health metrics.' },
  { "id": 72, "name": 'HEPA Air Purifier', "category": 'Health & Household', "price": 129.99, "imageUrl": 'https://picsum.photos/seed/airpurifierhome/400/300', "description": 'Captures 99.97% of dust, pollen, smoke, and pet dander in large rooms.' },
  { "id": 73, "name": 'Forehead Thermometer', "category": 'Health & Household', "price": 25.50, "imageUrl": 'https://picsum.photos/seed/thermometer/400/300', "description": 'A non-contact infrared thermometer for fast and accurate temperature readings.' },
  { "id": 74, "name": 'Reusable Food Storage Bags (10-Pack)', "category": 'Health & Household', "price": 19.99, "imageUrl": 'https://picsum.photos/seed/siliconebag/400/300', "description": 'Leakproof, freezer-safe silicone bags to reduce single-use plastic.' },
  { "id": 75, "name": 'All-Purpose Disinfecting Wipes (4-Pack)', "category": 'Health & Household', "price": 15.99, "imageUrl": 'https://picsum.photos/seed/wipes/400/300', "description": 'Kills 99.9% of viruses and bacteria on hard, non-porous surfaces.' },
  { "id": 76, "name": 'Electric Standing Desk Converter', "category": 'Health & Household', "price": 299.00, "imageUrl": 'https://picsum.photos/seed/standingdesk/400/300', "description": 'Motorized converter to easily switch between sitting and standing while you work.' },
  { "id": 77, "name": 'Essential Oil Diffuser', "category": 'Health & Household', "price": 39.99, "imageUrl": 'https://picsum.photos/seed/oildiffuser/400/300', "description": 'An ultrasonic aromatherapy diffuser with 7 ambient light settings.' },
  { "id": 78, "name": 'First Aid Kit (299 Pieces)', "category": 'Health & Household', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/firstaidkit/400/300', "description": 'A comprehensive first aid kit for home, car, or travel emergencies.' },
  { "id": 79, "name": 'High-Efficiency Laundry Detergent', "category": 'Health & Household', "price": 18.50, "imageUrl": 'https://picsum.photos/seed/laundrydetergent/400/300', "description": 'A plant-based, concentrated laundry detergent for up to 64 loads.' },
  { "id": 80, "name": 'Memory Foam Seat Cushion', "category": 'Health & Household', "price": 35.00, "imageUrl": 'https://picsum.photos/seed/seatcushion/400/300', "description": 'An orthopedic seat cushion for tailbone pain relief and improved posture.' },
  { "id": 81, "name": 'Portable Air Compressor Tire Inflator', "category": 'Automotive', "price": 45.99, "imageUrl": 'https://picsum.photos/seed/tireinflator/400/300', "description": 'A 12V DC air compressor with digital pressure gauge for cars and bikes.' },
  { "id": 82, "name": '4K Dash Cam Front and Rear', "category": 'Automotive', "price": 129.99, "imageUrl": 'https://picsum.photos/seed/dashcam/400/300', "description": 'Dual dash cam with night vision, GPS, and a G-sensor for accident recording.' },
  { "id": 83, "name": 'Car Vacuum Cleaner High Power', "category": 'Automotive', "price": 36.99, "imageUrl": 'https://picsum.photos/seed/carvacuum/400/300', "description": 'A powerful, portable handheld vacuum for cleaning car interiors.' },
  { "id": 84, "name": 'Bluetooth FM Transmitter for Car', "category": 'Automotive', "price": 19.99, "imageUrl": 'https://picsum.photos/seed/fmtransmitter/400/300', "description": 'Allows you to stream music and calls from your phone to your car stereo.' },
  { "id": 85, "name": 'Compact Car Jump Starter', "category": 'Automotive', "price": 79.99, "imageUrl": 'https://picsum.photos/seed/jumpstarter/400/300', "description": 'A portable lithium battery booster pack for starting dead car batteries.' },
  { "id": 86, "name": 'Weatherproof Car Cover', "category": 'Automotive', "price": 59.99, "imageUrl": 'https://picsum.photos/seed/carcover/400/300', "description": 'A 6-layer heavy-duty car cover for all-weather protection.' },
  { "id": 87, "name": 'Digital Tire Pressure Gauge', "category": 'Automotive', "price": 12.99, "imageUrl": 'https://picsum.photos/seed/pressuregauge/400/300', "description": 'An easy-to-use digital gauge for accurate tire pressure readings.' },
  { "id": 88, "name": 'Car Trunk Organizer', "category": 'Automotive', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/trunkorganizer/400/300', "description": 'A heavy-duty, collapsible organizer with multiple compartments.' },
  { "id": 89, "name": 'Windshield Sun Shade', "category": 'Automotive', "price": 17.99, "imageUrl": 'https://picsum.photos/seed/carsunshade/400/300', "description": 'A foldable sun shade to keep your car interior cool and protect from UV rays.' },
  { "id": 90, "name": 'Microfiber Cleaning Cloths (12-Pack)', "category": 'Automotive', "price": 15.99, "imageUrl": 'https://picsum.photos/seed/microfibercloth/400/300', "description": 'Ultra-soft, scratch-free cloths for washing, drying, and detailing.' },
  { "id": 91, "name": 'Automatic Pet Feeder', "category": 'Pet Supplies', "price": 69.99, "imageUrl": 'https://picsum.photos/seed/petfeeder/400/300', "description": 'A smart feeder with a timer and portion control for cats and dogs.' },
  { "id": 92, "name": 'Pet Grooming Glove', "category": 'Pet Supplies', "price": 14.99, "imageUrl": 'https://picsum.photos/seed/petgrooming/400/300', "description": 'A gentle de-shedding brush glove for long and short-haired pets.' },
  { "id": 93, "name": 'Orthopedic Dog Bed', "category": 'Pet Supplies', "price": 59.99, "imageUrl": 'https://picsum.photos/seed/dogbed/400/300', "description": 'A memory foam dog bed with a washable cover for joint support.' },
  { "id": 94, "name": 'Interactive Cat Toy with Butterfly', "category": 'Pet Supplies', "price": 18.99, "imageUrl": 'https://picsum.photos/seed/cattoy/400/300', "description": 'An electronic rotating butterfly toy to engage your cat\'s hunting instincts.' },
  { "id": 95, "name": 'Heavy-Duty Retractable Dog Leash', "category": 'Pet Supplies', "price": 24.99, "imageUrl": 'https://picsum.photos/seed/dogleash/400/300', "description": 'A 16-foot retractable leash with an anti-slip handle for dogs up to 110 lbs.' },
  { "id": 96, "name": 'Pet Water Fountain', "category": 'Pet Supplies', "price": 32.99, "imageUrl": 'https://picsum.photos/seed/petfountain/400/300', "description": 'A 2.5L automatic water fountain to encourage pets to drink more.' },
  { "id": 97, "name": 'Natural Dental Chews for Dogs (22-Count)', "category": 'Pet Supplies', "price": 19.99, "imageUrl": 'https://picsum.photos/seed/dogtreats/400/300', "description": 'Grain-free dental treats to help clean teeth and freshen breath.' },
  { "id": 98, "name": 'Cat Tree with Scratching Posts', "category": 'Pet Supplies', "price": 89.99, "imageUrl": 'https://picsum.photos/seed/cattree/400/300', "description": 'A multi-level cat tower with condos, perches, and sisal scratching posts.' },
  { "id": 99, "name": 'Portable Pet Carrier', "category": 'Pet Supplies', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/petcarrier/400/300', "description": 'An airline-approved soft-sided carrier for small dogs and cats.' },
  { "id": 100, "name": 'Pet Waste Bags with Dispenser', "category": 'Pet Supplies', "price": 12.99, "imageUrl": 'https://picsum.photos/seed/dogwastebag/400/300', "description": '900-count of leak-proof, lavender-scented pet waste bags.' },
  { "id": 101, "name": '8-Piece Garden Tool Set', "category": 'Garden & Outdoor', "price": 39.99, "imageUrl": 'https://picsum.photos/seed/gardentools/400/300', "description": 'A heavy-duty set including a trowel, weeder, and cultivator with an ergonomic design.' },
  { "id": 102, "name": 'Expandable Garden Hose', "category": 'Garden & Outdoor', "price": 45.99, "imageUrl": 'https://picsum.photos/seed/gardenhose/400/300', "description": 'A 50-foot flexible, lightweight hose with a 10-function spray nozzle.' },
  { "id": 103, "name": 'Outdoor Propane Fire Pit Table', "category": 'Garden & Outdoor', "price": 299.99, "imageUrl": 'https://picsum.photos/seed/firepit/400/300', "description": 'A 50,000 BTU auto-ignition fire pit for a cozy backyard ambiance.' },
  { "id": 104, "name": 'Solar Powered Pathway Lights (8-Pack)', "category": 'Garden & Outdoor', "price": 35.99, "imageUrl": 'https://picsum.photos/seed/solarlight/400/300', "description": 'Bright, waterproof solar lights for illuminating walkways and gardens.' },
  { "id": 105, "name": 'Gardening Gloves with Claws', "category": 'Garden & Outdoor', "price": 13.99, "imageUrl": 'https://picsum.photos/seed/gardeninggloves/400/300', "description": 'Durable, waterproof gloves with built-in claws for easy digging and planting.' },
  { "id": 106, "name": 'Electric Leaf Blower', "category": 'Garden & Outdoor', "price": 89.00, "imageUrl": 'https://picsum.photos/seed/leafblower/400/300', "description": 'A powerful corded leaf blower, vacuum, and mulcher in one.' },
  { "id": 107, "name": 'Bird Feeder with Steel Hanger', "category": 'Garden & Outdoor', "price": 24.99, "imageUrl": 'https://picsum.photos/seed/birdfeeder/400/300', "description": 'A squirrel-proof hanging bird feeder to attract a variety of wild birds.' },
  { "id": 108, "name": 'Heavy-Duty Waterproof Grill Cover', "category": 'Garden & Outdoor', "price": 29.99, "imageUrl": 'https://picsum.photos/seed/grillcover/400/300', "description": 'A durable cover to protect your BBQ grill from rain, snow, and sun.' },
  { "id": 109, "name": 'Folding Camping Chair', "category": 'Garden & Outdoor', "price": 34.99, "imageUrl": 'https://picsum.photos/seed/campingchair/400/300', "description": 'A portable quad chair with a built-in cooler and cup holder.' },
  { "id": 110, "name": 'Raised Garden Bed', "category": 'Garden & Outdoor', "price": 55.00, "imageUrl": 'https://picsum.photos/seed/raisedgardenbed/400/300', "description": 'A galvanized steel planter box for growing vegetables, herbs, and flowers.' },
  { "id": 111, "name": '20V Cordless Drill Driver Kit', "category": 'Tools & Home Improvement', "price": 99.00, "imageUrl": 'https://picsum.photos/seed/cordlessdrill/400/300', "description": 'A powerful cordless drill with two batteries, a charger, and a 30-piece bit set.' },
  { "id": 112, "name": '165-Piece Home Repair Tool Kit', "category": 'Tools & Home Improvement', "price": 75.99, "imageUrl": 'https://picsum.photos/seed/toolkit/400/300', "description": 'A comprehensive tool set for most small repairs and DIY projects around the house.' },
  { "id": 113, "name": 'Digital Laser Measure', "category": 'Tools & Home Improvement', "price": 49.99, "imageUrl": 'https://picsum.photos/seed/lasermeasure/400/300', "description": 'A 165-foot laser distance meter for accurate and fast measurements.' },
  { "id": 114, "name": 'Smart Wi-Fi Light Switch (4-Pack)', "category": 'Tools & Home Improvement', "price": 42.99, "imageUrl": 'https://picsum.photos/seed/lightswitch/400/300', "description": 'Control your lights from anywhere with your smartphone, Alexa, or Google Assistant.' },
  { "id": 115, "name": 'Magnetic Wristband for Screws', "category": 'Tools & Home Improvement', "price": 15.99, "imageUrl": 'https://picsum.photos/seed/magneticwristband/400/300', "description": 'A handy wristband with powerful magnets for holding screws, nails, and drill bits.' },
  { "id": 116, "name": 'Heavy-Duty 6-Outlet Power Strip', "category": 'Tools & Home Improvement', "price": 22.50, "imageUrl": 'https://picsum.photos/seed/powerstrip/400/300', "description": 'A surge protector power strip with a 10-foot cord and wall mount capability.' },
  { "id": 117, "name": 'LED Garage Lights', "category": 'Tools & Home Improvement', "price": 39.99, "imageUrl": 'https://picsum.photos/seed/garagelight/400/300', "description": 'Deformable, ultra-bright LED ceiling lights for garages and workshops.' },
  { "id": 118, "name": 'Self-Leveling Laser Level', "category": 'Tools & Home Improvement', "price": 55.00, "imageUrl": 'https://picsum.photos/seed/laserlevel/400/300', "description": 'A cross-line laser level for picture hanging, construction, and wallpapering.' },
  { "id": 119, "name": 'Non-Slip Step Ladder', "category": 'Tools & Home Improvement', "price": 65.00, "imageUrl": 'https://picsum.photos/seed/stepladder/400/300', "description": 'A 3-step folding steel ladder with a convenient tool pouch.' },
  { "id": 120, "name": 'Digital Caliper', "category": 'Tools & Home Improvement', "price": 28.99, "imageUrl": 'https://picsum.photos/seed/digitalcaliper/400/300', "description": 'A stainless steel electronic vernier caliper for precise inside/outside measurements.' },
  { "id": 121, "name": 'High-Back Ergonomic Office Chair', "category": 'Office Products', "price": 249.99, "imageUrl": 'https://picsum.photos/seed/officechair/400/300', "description": 'Adjustable mesh office chair with lumbar support and flip-up arms.' },
  { "id": 122, "name": 'Dual Monitor Stand', "category": 'Office Products', "price": 45.99, "imageUrl": 'https://picsum.photos/seed/monitorstand/400/300', "description": 'A height-adjustable gas spring monitor arm for two screens up to 27 inches.' },
  { "id": 123, "name": 'Wireless Keyboard and Mouse Combo', "category": 'Office Products', "price": 39.99, "imageUrl": 'https://picsum.photos/seed/wirelesskeyboard/400/300', "description": 'A sleek, quiet, full-size keyboard and mouse with a single USB receiver.' },
  { "id": 124, "name": 'Desktop Whiteboard', "category": 'Office Products', "price": 25.99, "imageUrl": 'https://picsum.photos/seed/desktopwhiteboard/400/300', "description": 'A glass dry-erase board with built-in storage for markers and accessories.' },
  { "id": 125, "name": 'High-Speed Paper Shredder', "category": 'Office Products', "price": 89.99, "imageUrl": 'https://picsum.photos/seed/papershredder/400/300', "description": 'A 12-sheet cross-cut shredder for paper, credit cards, and staples.' },
  { "id": 126, "name": 'Noise Cancelling Headset with Microphone', "category": 'Office Products', "price": 69.99, "imageUrl": 'https://picsum.photos/seed/headsetmicrophone/400/300', "description": 'A USB headset perfect for online meetings, webinars, and call centers.' },
  { "id": 127, "name": 'Laminator Machine with Sheets', "category": 'Office Products', "price": 42.00, "imageUrl": 'https://picsum.photos/seed/laminator/400/300', "description": 'A thermal laminator for home and office use, includes 20 laminating pouches.' },
  { "id": 128, "name": 'Under Desk Foot Rest', "category": 'Office Products', "price": 32.50, "imageUrl": 'https://picsum.photos/seed/footrest/400/300', "description": 'An ergonomic memory foam footrest to improve posture and circulation.' },
  { "id": 129, "name": 'Gel Pens (36-Color Set)', "category": 'Office Products', "price": 18.99, "imageUrl": 'https://picsum.photos/seed/gelpens/400/300', "description": 'A vibrant set of fine-point gel ink pens for journaling, note-taking, and drawing.' },
  { "id": 130, "name": 'Cable Management Box (Set of 2)', "category": 'Office Products', "price": 21.99, "imageUrl": 'https://picsum.photos/seed/cablemanagement/400/300', "description": 'Organize and hide messy power strips and cords for a cleaner workspace.' },
  { "id": 131, "name": 'Organic Extra Virgin Olive Oil', "category": 'Grocery & Gourmet Food', "price": 19.99, "imageUrl": 'https://picsum.photos/seed/oliveoil/400/300', "description": 'Cold-pressed, single-origin olive oil from Italy, perfect for salads and cooking.' },
  { "id": 132, "name": 'Gourmet Coffee Beans (2lb Bag)', "category": 'Grocery & Gourmet Food', "price": 28.50, "imageUrl": 'https://picsum.photos/seed/coffeebeans/400/300', "description": 'A medium-roast whole bean coffee with notes of caramel and chocolate.' },
  { "id": 133, "name": 'Artisanal Sourdough Bread', "category": 'Grocery & Gourmet Food', "price": 9.50, "imageUrl": 'https://picsum.photos/seed/sourdoughbread/400/300', "description": 'A crusty, freshly baked sourdough loaf made with organic flour.' },
  { "id": 134, "name": 'Assorted Herbal Tea Box (48 Count)', "category": 'Grocery & Gourmet Food', "price": 15.99, "imageUrl": 'https://picsum.photos/seed/herbaltea/400/300', "description": 'A collection of 6 different caffeine-free herbal tea flavors.' },
  { "id": 135, "name": 'Pure Maple Syrup, Grade A', "category": 'Grocery & Gourmet Food', "price": 14.99, "imageUrl": 'https://picsum.photos/seed/maplesyrup/400/300', "description": 'Amber color, rich taste maple syrup sourced from Vermont.' },
  { "id": 136, "name": 'Spicy Hot Sauce Variety Pack', "category": 'Grocery & Gourmet Food', "price": 24.99, "imageUrl": 'https://picsum.photos/seed/hotsauce/400/300', "description": 'A gift set of 4 different hot sauces, from mild to extra hot.' },
  { "id": 137, "name": 'Organic Quinoa (2lb Bag)', "category": 'Grocery & Gourmet Food', "price": 12.99, "imageUrl": 'https://picsum.photos/seed/quinoa/400/300', "description": 'A pre-washed, gluten-free superfood packed with protein and fiber.' },
  { "id": 138, "name": 'Dark Chocolate Sea Salt Caramels', "category": 'Grocery & Gourmet Food', "price": 18.00, "imageUrl": 'https://picsum.photos/seed/chocolatecaramels/400/300', "description": 'A luxurious box of handcrafted caramels covered in dark chocolate.' },
  { "id": 139, "name": 'Balsamic Glaze of Modena', "category": 'Grocery & Gourmet Food', "price": 11.99, "imageUrl": 'https://picsum.photos/seed/balsamicglaze/400/300', "description": 'A thick, sweet glaze perfect for drizzling over meats, cheeses, and salads.' },
  { "id": 140, "name": 'Truffle-Infused Sea Salt', "category": 'Grocery & Gourmet Food', "price": 16.50, "imageUrl": 'https://picsum.photos/seed/trufflesalt/400/300', "description": 'An aromatic finishing salt to elevate any dish with the flavor of black truffles.' },
  { "id": 141, "name": 'Acoustic Guitar Starter Pack', "category": 'Musical Instruments', "price": 149.99, "imageUrl": 'https://picsum.photos/seed/acousticguitar/400/300', "description": 'A full-size dreadnought acoustic guitar with a gig bag, tuner, and picks.' },
  { "id": 142, "name": '88-Key Digital Piano', "category": 'Musical Instruments', "price": 450.00, "imageUrl": 'https://picsum.photos/seed/digitalpiano/400/300', "description": 'A digital piano with weighted keys, a music stand, and a sustain pedal.' },
  { "id": 143, "name": 'Portable Electronic Drum Kit', "category": 'Musical Instruments', "price": 299.99, "imageUrl": 'https://picsum.photos/seed/electronicdrums/400/300', "description": 'A roll-up drum pad with built-in speakers, drumsticks, and pedals.' },
  { "id": 144, "name": 'Concert Ukulele Kit', "category": 'Musical Instruments', "price": 69.99, "imageUrl": 'https://picsum.photos/seed/ukulele/400/300', "description": 'A mahogany ukulele with a gig bag, strap, and online lessons.' },
  { "id": 145, "name": 'USB Studio Condenser Microphone', "category": 'Musical Instruments', "price": 89.00, "imageUrl": 'https://picsum.photos/seed/studiomicrophone/400/300', "description": 'A plug-and-play microphone for podcasting, streaming, and home recording.' },
  { "id": 146, "name": 'Harmonica, Key of C', "category": 'Musical Instruments', "price": 19.99, "imageUrl": 'https://picsum.photos/seed/harmonica/400/300', "description": 'A 10-hole diatonic harmonica for blues, folk, and rock music.' },
  { "id": 147, "name": 'MIDI Keyboard Controller', "category": 'Musical Instruments', "price": 119.00, "imageUrl": 'https://picsum.photos/seed/midikeyboard/400/300', "description": 'A 25-key USB MIDI controller with drum pads and assignable knobs.' },
  { "id": 148, "name": 'Violin Starter Kit (4/4 Full Size)', "category": 'Musical Instruments', "price": 129.99, "imageUrl": 'https://picsum.photos/seed/violin/400/300', "description": 'A complete violin outfit with a case, bow, rosin, and shoulder rest.' },
  { "id": 149, "name": 'Adjustable Music Stand', "category": 'Musical Instruments', "price": 28.99, "imageUrl": 'https://picsum.photos/seed/musicstand/400/300', "description": 'A portable, folding music stand with a carrying bag.' },
  { "id": 150, "name": 'Metronome Tuner Combo', "category": 'Musical Instruments', "price": 24.99, "imageUrl": 'https://picsum.photos/seed/metronome/400/300', "description": 'A digital 3-in-1 device for tuning instruments and keeping time.' }
]

def create_database():
    # Check if the database file already exists. If so, do nothing.
    if os.path.exists(DATABASE_FILE):
        print(f"Database '{DATABASE_FILE}' already exists. Skipping creation.")
        return
        
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Create the products table
        cursor.execute("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                imageUrl TEXT,
                description TEXT
            );
        """)

        # Insert product data into the table
        for product in PRODUCTS_DATA:
            cursor.execute("""
                INSERT INTO products (id, name, category, price, imageUrl, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                product['id'],
                product['name'],
                product['category'],
                product['price'],
                product['imageUrl'],
                product['description']
            ))

        conn.commit()
        print(f"Database '{DATABASE_FILE}' created and populated with {len(PRODUCTS_DATA)} products successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_database()