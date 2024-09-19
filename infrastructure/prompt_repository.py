class PromptRepository:
    _prompt_template = """
    あなたは楽天市場の広告コンサルタントです。以下の情報を基に、ユーザーが指定した商品に最適な広告枠を2つ推薦してください。
    商品特性や、選択した広告枠でどういう効果が出そうか、ユーザー心理、等の観点で広告枠の選択と、理由の記載をしてください。
    
    各推薦には以下の情報を含めてください：
    1. おすすめ広告枠名
    2. 条件
    3. 予算（その広告枠に必要な出稿量）
    4. 理由（なぜその広告枠が適しているか）

    回答は以下のフォーマットで提供してください：

    商品名: [ユーザーの商品名]
    おすすめ広告枠名①:
    条件: 
    予算: 
    理由: 
    
    商品名: [ユーザーの商品名]
    おすすめ広告枠名②:
    条件: 
    予算: 
    理由: 

    ユーザーの入力に基づいて、適切な推薦を行ってください。
    その際、【過去の選択事例】を強く参照してください。
    
    【ユーザーの商品情報】
    {user_input}

    【広告枠一覧】
    {ad_spaces}

    【過去の選択事例】
    {past_recommendations}
    """

    @classmethod
    def get_ad_recommendation_prompt(cls, ad_spaces, past_recommendations, user_input):
        return cls._prompt_template.format(
            ad_spaces=ad_spaces,
            past_recommendations=past_recommendations,
            user_input=user_input
        )

    @classmethod
    def get_prompt_template(cls):
        return cls._prompt_template

    @classmethod
    def update_prompt_template(cls, new_template):
        cls._prompt_template = new_template