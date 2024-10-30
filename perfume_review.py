import sqlite3

def search_perfume(perfume_name):
    conn = sqlite3.connect('fragranceFitter.db')
    c = conn.cursor()
    c.execute('SELECT name, brand, image_url FROM perfumes WHERE name LIKE ?', ('%' + perfume_name + '%',))
    results = c.fetchall()
    conn.close()
    
    perfumes = []
    for result in results:
        perfumes.append({
            'name': result[0],
            'brand': result[1],
            'image_url': result[2]
        })
    
    return perfumes

def add_review(perfume_name, user_name, review, date):
    conn = sqlite3.connect('fragranceFitter.db')
    c = conn.cursor()
    c.execute('SELECT id FROM perfumes WHERE name = ?', (perfume_name,))
    result = c.fetchone()
    if result:
        perfume_id = result[0]
        c.execute('INSERT INTO reviews (perfume_id, user_name, reviews) VALUES (?, ?, ?)', (perfume_id, user_name, review))
        conn.commit()
    conn.close()


def get_recent_reviews():
    conn = sqlite3.connect('fragranceFitter.db')
    c = conn.cursor()
    # Ensure perfumes table has a column for image URLs, e.g., image_url
    c.execute('''
        SELECT perfumes.name, reviews.user_name, reviews.reviews, reviews.date_posted, perfumes.image_url 
        FROM reviews 
        INNER JOIN perfumes ON reviews.perfume_id = perfumes.id 
        ORDER BY reviews.id DESC 
        LIMIT 5
    ''')
    results = c.fetchall()
    conn.close()
    
    reviews = []
    for result in results:
        reviews.append({
            'perfume_name': result[0],
            'user_name': result[1],
            'review': result[2],
            'date_posted': result[3],
            'image_url': result[4]  # Include image URL in the response
        })
    
    return reviews
