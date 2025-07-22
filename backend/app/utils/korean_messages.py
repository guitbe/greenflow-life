"""
한국어 UX 메시지 유틸리티
톤앤매너: 친절하고 격려하는 말투, 위협적이거나 수치심 유발하지 않음
"""

import random
from datetime import datetime
from typing import Dict, List, Optional

class KoreanMessageGenerator:
    """한국어 UX 메시지 생성기"""
    
    def __init__(self):
        self.greeting_messages = {
            "morning": [
                "좋은 아침이에요! 오늘도 지구를 지키는 하루 되세요 🌅",
                "상쾌한 아침이네요! 오늘은 어떤 맛있는 선택을 하실 건가요? ☀️",
                "새로운 하루의 시작! 환경을 생각하는 식사로 시작해보세요 🌱"
            ],
            "afternoon": [
                "오늘 하루도 수고 많으셨어요! 점심은 맛있게 드셨나요? 😊",
                "따뜻한 오후네요! 오늘의 식사는 어떠셨는지 궁금해요 🍽️",
                "점심시간이 기다려지는 오후예요! 맛있는 선택 하세요 ✨"
            ],
            "evening": [
                "하루 마무리 잘 하고 계시나요? 저녁 식사도 기록해보세요 🌙",
                "편안한 저녁 시간이에요! 오늘 하루 정말 고생하셨어요 💚",
                "저녁노을이 아름다운 시간이네요! 오늘의 마지막 식사는? 🌆"
            ]
        }
        
        self.success_messages = {
            "meal_logged": [
                "훌륭해요! 오늘도 지구를 지키는 선택을 하셨네요 🌍",
                "멋진 기록이에요! 작은 실천이 큰 변화를 만듭니다 ✨",
                "잘하셨어요! 꾸준한 기록이 미래를 바꿔나가요 👏",
                "완벽해요! 이런 관심이 지구를 건강하게 만들어요 💚",
                "대단해요! 환경을 생각하는 여러분의 마음이 아름다워요 🌱"
            ],
            "swap_accepted": [
                "와! 정말 현명한 선택이에요! 지구가 미소짓고 있을 거예요 😊",
                "훌륭한 결정이에요! 이런 작은 변화가 세상을 바꿔나가요 🌍",
                "멋져요! 환경을 생각하는 선택에 박수를 보내드려요 👏",
                "좋은 선택이에요! 미래 세대가 고마워할 거예요 🌱",
                "완벽해요! 지속 가능한 미래를 함께 만들어가요 ✨"
            ],
            "challenge_completed": [
                "축하해요! 챌린지 완성! 정말 자랑스러워요 🎉",
                "와! 해내셨네요! 이런 노력이 진짜 멋져요 🏆",
                "대성공! 꾸준한 노력의 결과네요! 👑",
                "완벽해요! 도전 정신이 빛나는 순간이에요 ⭐",
                "훌륭해요! 이런 실천력이 세상을 바꿔나가요 💪"
            ]
        }
        
        self.encouragement_messages = {
            "low_carbon_choice": [
                "지금 선택하신 음식, 지구에게 정말 좋은 선택이에요! 🌿",
                "환경을 생각한 멋진 선택이네요! 계속 이렇게 해주세요 💚",
                "친환경 식단 실천! 작은 변화가 큰 의미를 만들어요 🌱",
                "지구를 사랑하는 마음이 느껴져요! 고마워요 🌍"
            ],
            "improvement_needed": [
                "괜찮아요! 완벽하지 않아도 돼요. 조금씩 나아가면 되니까요 😊",
                "시작이 반이에요! 이미 환경을 생각하고 계시니까요 ✨",
                "천천히 해도 괜찮아요! 꾸준함이 더 중요해요 🐢",
                "작은 변화부터 시작해보세요! 여러분을 응원해요 💪",
                "실수는 성장의 기회예요! 다음엔 더 좋은 선택하실 거예요 🌱"
            ],
            "streak_motivation": [
                "연속 기록 대단해요! 이런 꾸준함이 변화를 만들어요 🔥",
                "매일매일 실천하는 모습이 정말 멋져요! 계속해주세요 📅",
                "꾸준한 기록! 습관의 힘을 보여주고 계시네요 💪",
                "중단 없는 실천! 진정한 환경 지킴이시네요 👑"
            ]
        }
        
        self.insight_messages = {
            "carbon_savings": [
                "와! 지금까지 {amount}kg의 탄소를 절약하셨어요! 나무 {trees}그루를 심은 효과예요 🌳",
                "대단해요! {amount}kg 탄소 절약은 자동차 {km}km 덜 타기와 같은 효과예요 🚗",
                "훌륭해요! {amount}kg의 탄소를 줄이셨네요! 지구가 숨쉬기 편해졌어요 🌍"
            ],
            "weekly_summary": [
                "이번 주도 수고하셨어요! {meals}번의 기록으로 {carbon}kg 탄소를 절약했어요 📊",
                "한 주 동안 {meals}번 기록하며 환경을 생각해주셨네요! 고마워요 💚",
                "일주일 요약: {meals}번의 선택으로 {carbon}kg 탄소 절약! 멋져요 ✨"
            ],
            "milestone_reached": [
                "축하해요! {milestone} 달성! 정말 자랑스러운 순간이에요 🎉",
                "와! {milestone} 완성! 이런 성취가 세상을 바꿔나가요 🏆",
                "대단해요! {milestone} 도달! 꾸준한 노력의 결실이네요 👏"
            ]
        }
        
        self.tips_messages = [
            "💡 소고기 대신 닭고기를 선택하면 50% 이상 탄소를 절약할 수 있어요!",
            "🌱 제철 음식을 선택하면 맛도 좋고 환경에도 좋아요!",
            "🐟 일주일에 2번 생선 요리를 먹으면 탄소 발자국을 크게 줄일 수 있어요!",
            "🥬 채소를 더 많이 먹으면 건강과 환경, 두 마리 토끼를 잡을 수 있어요!",
            "♻️ 음식물 쓰레기를 줄이는 것도 탄소 절약의 중요한 방법이에요!",
            "🌾 통곡물을 선택하면 영양도 풍부하고 환경에도 도움이 돼요!",
            "🍄 버섯류는 단백질도 풍부하고 탄소 발자국이 낮은 훌륭한 식재료예요!",
            "🥗 로컬 푸드를 선택하면 운송 과정의 탄소 배출을 줄일 수 있어요!"
        ]

    def get_greeting_message(self) -> str:
        """시간대별 인사말 반환"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_category = "morning"
        elif 12 <= hour < 18:
            time_category = "afternoon"
        else:
            time_category = "evening"
            
        return random.choice(self.greeting_messages[time_category])
    
    def get_success_message(self, action_type: str) -> str:
        """성공 메시지 반환"""
        messages = self.success_messages.get(action_type, self.success_messages["meal_logged"])
        return random.choice(messages)
    
    def get_encouragement_message(self, context: str) -> str:
        """격려 메시지 반환"""
        messages = self.encouragement_messages.get(context, self.encouragement_messages["low_carbon_choice"])
        return random.choice(messages)
    
    def get_insight_message(self, insight_type: str, **kwargs) -> str:
        """인사이트 메시지 반환"""
        messages = self.insight_messages.get(insight_type, [])
        if not messages:
            return "계속해서 환경을 생각해주셔서 감사해요! 🌍"
        
        template = random.choice(messages)
        try:
            return template.format(**kwargs)
        except KeyError:
            return template
    
    def get_tip_message(self) -> str:
        """랜덤 팁 메시지 반환"""
        return random.choice(self.tips_messages)
    
    def get_personalized_recommendation_message(
        self, 
        user_name: str = "",
        food_from: str = "",
        food_to: str = "",
        carbon_reduction: float = 0,
        meal_pattern: str = ""
    ) -> str:
        """개인화된 추천 메시지 생성"""
        
        base_messages = [
            f"{food_to}로 바꾸면 {carbon_reduction:.0f}% 탄소를 절약할 수 있어요!",
            f"{food_to}는 맛도 좋고 환경에도 좋은 선택이에요!",
            f"{food_to}로 건강하고 친환경적인 식사를 해보세요!",
        ]
        
        # 패턴 기반 개인화
        if meal_pattern == "meat_lover":
            personalized_part = " 고기 요리를 자주 드시는군요! 가끔은 이런 선택도 어떠세요? 😊"
        elif meal_pattern == "health_conscious":
            personalized_part = " 건강을 생각하시는 분이시군요! 이 선택이 더 도움이 될 거예요 💪"
        elif meal_pattern == "frequent_logger":
            personalized_part = " 꾸준한 기록 습관이 멋져요! 이런 선택으로 더 발전해보세요 🌟"
        else:
            personalized_part = " 환경을 생각하는 마음이 아름다워요! 💚"
        
        base_message = random.choice(base_messages)
        return base_message + personalized_part
    
    def get_error_message(self, error_type: str) -> str:
        """에러 메시지 반환 (격려하는 톤으로)"""
        error_messages = {
            "network_error": "잠시 연결이 원활하지 않네요. 조금 후에 다시 시도해주세요! 😊",
            "validation_error": "앗! 입력하신 내용을 다시 한번 확인해주세요 ✨",
            "server_error": "서버에 작은 문제가 있네요. 금방 해결될 거예요! 잠시만 기다려주세요 🙏",
            "not_found": "찾으시는 내용을 찾을 수 없어요. 다른 방법으로 시도해보세요! 💡",
            "general": "예상치 못한 일이 발생했네요. 다시 시도해주시면 될 거예요! 화이팅! 💪"
        }
        
        return error_messages.get(error_type, error_messages["general"])

# 전역 메시지 생성기 인스턴스
korean_messages = KoreanMessageGenerator()

def get_korean_message(category: str, message_type: str = "", **kwargs) -> str:
    """한국어 메시지 조회 헬퍼 함수"""
    if category == "greeting":
        return korean_messages.get_greeting_message()
    elif category == "success":
        return korean_messages.get_success_message(message_type)
    elif category == "encouragement":
        return korean_messages.get_encouragement_message(message_type)
    elif category == "insight":
        return korean_messages.get_insight_message(message_type, **kwargs)
    elif category == "tip":
        return korean_messages.get_tip_message()
    elif category == "error":
        return korean_messages.get_error_message(message_type)
    elif category == "recommendation":
        return korean_messages.get_personalized_recommendation_message(**kwargs)
    else:
        return "함께 지구를 지켜나가요! 🌍✨" 