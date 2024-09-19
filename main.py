from application.ad_recommender_service import AdRecommenderService

if __name__ == "__main__":
    recommender_service = AdRecommenderService()
    ad_spaces = recommender_service.load_csv('広告枠一覧 - 広告枠.csv')
    past_recommendations = recommender_service.load_csv('広告枠一覧 - 広告枠、商品、理由.csv')
    
    # ユーザー入力を受け取る
    user_input = input("商品情報を入力してください：\n")

    recommendations = recommender_service.get_recommendations(user_input, ad_spaces, past_recommendations)
    print(recommendations)