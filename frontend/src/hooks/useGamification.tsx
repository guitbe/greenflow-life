import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { Trophy, Star, Target, Zap, Gift } from 'lucide-react';

interface Achievement {
  id: string;
  type: 'badge' | 'milestone' | 'streak' | 'challenge';
  title: string;
  message: string;
  icon: string;
  points?: number;
  rarity?: 'common' | 'rare' | 'epic' | 'legendary';
}

interface ProgressUpdate {
  type: 'carbon_saved' | 'meal_logged' | 'swap_accepted' | 'challenge_joined' | 'streak_extended';
  value: number;
  message: string;
  celebration?: boolean;
}

interface GamificationState {
  totalPoints: number;
  currentStreak: number;
  totalCarbonSaved: number;
  achievements: Achievement[];
  recentActivities: ProgressUpdate[];
}

const achievementIcons = {
  badge: '🏅',
  milestone: '🎯',
  streak: '🔥',
  challenge: '🏆'
};

const rarityColors = {
  common: { bg: 'bg-gray-100', border: 'border-gray-300', text: 'text-gray-700' },
  rare: { bg: 'bg-blue-100', border: 'border-blue-300', text: 'text-blue-700' },
  epic: { bg: 'bg-purple-100', border: 'border-purple-300', text: 'text-purple-700' },
  legendary: { bg: 'bg-yellow-100', border: 'border-yellow-300', text: 'text-yellow-700' }
};

export const useGamification = () => {
  const [state, setState] = useState<GamificationState>({
    totalPoints: 0,
    currentStreak: 0,
    totalCarbonSaved: 0,
    achievements: [],
    recentActivities: []
  });

  // 성취 달성 시 호출
  const triggerAchievement = useCallback((achievement: Achievement) => {
    setState(prev => ({
      ...prev,
      achievements: [...prev.achievements, achievement]
    }));

    const rarity = achievement.rarity || 'common';
    const colors = rarityColors[rarity];

    // 성취 애니메이션 토스트
    toast.custom((t) => (
      <motion.div
        initial={{ scale: 0, rotate: 180, opacity: 0 }}
        animate={{ 
          scale: t.visible ? 1 : 0, 
          rotate: t.visible ? 0 : 180,
          opacity: t.visible ? 1 : 0 
        }}
        transition={{ 
          type: "spring", 
          stiffness: 200, 
          damping: 20 
        }}
        className={`max-w-md w-full ${colors.bg} shadow-lg rounded-xl pointer-events-auto flex ring-1 ${colors.border} p-4`}
      >
        <div className="flex-1 w-0">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <motion.div
                animate={{ 
                  rotate: [0, 10, -10, 0],
                  scale: [1, 1.1, 1.1, 1]
                }}
                transition={{ 
                  duration: 0.5,
                  repeat: 2
                }}
                className="text-3xl"
              >
                {achievement.icon || achievementIcons[achievement.type]}
              </motion.div>
            </div>
            <div className="ml-3 flex-1">
              <div className="flex items-center gap-2">
                <Trophy className={`w-5 h-5 ${colors.text}`} />
                <p className={`text-sm font-bold ${colors.text}`}>
                  새로운 성취! 🎉
                </p>
              </div>
              <p className="text-lg font-semibold text-gray-900 mt-1">
                {achievement.title}
              </p>
              <p className="text-sm text-gray-600 mt-1">
                {achievement.message}
              </p>
              {achievement.points && (
                <div className="flex items-center gap-1 mt-2">
                  <Star className="w-4 h-4 text-yellow-500" />
                  <span className="text-sm font-medium text-yellow-600">
                    +{achievement.points} 포인트
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="flex border-l border-gray-200">
          <button
            onClick={() => toast.dismiss(t.id)}
            className="w-full border border-transparent rounded-none rounded-r-lg p-4 flex items-center justify-center text-sm font-medium text-gray-500 hover:text-gray-600 focus:outline-none"
          >
            닫기
          </button>
        </div>
      </motion.div>
    ), {
      duration: 5000,
      position: 'top-center'
    });

    // 포인트 업데이트
    if (achievement.points) {
      setState(prev => ({
        ...prev,
        totalPoints: prev.totalPoints + achievement.points!
      }));
    }
  }, []);

  // 진행 상황 업데이트
  const updateProgress = useCallback((update: ProgressUpdate) => {
    setState(prev => ({
      ...prev,
      recentActivities: [update, ...prev.recentActivities.slice(0, 9)] // 최근 10개만 유지
    }));

    // 특별한 성취나 축하가 필요한 경우
    if (update.celebration) {
      toast.success(update.message, {
        icon: '🎉',
        duration: 3000,
        style: {
          background: '#10B981',
          color: '#ffffff',
          fontWeight: 'bold'
        }
      });
    } else {
      // 일반적인 진행 상황 업데이트
      toast.success(update.message, {
        icon: getProgressIcon(update.type),
        duration: 2000
      });
    }

    // 특정 업데이트에 따른 상태 변경
    switch (update.type) {
      case 'carbon_saved':
        setState(prev => ({
          ...prev,
          totalCarbonSaved: prev.totalCarbonSaved + update.value
        }));
        break;
      case 'streak_extended':
        setState(prev => ({
          ...prev,
          currentStreak: Math.max(prev.currentStreak, update.value)
        }));
        break;
    }
  }, []);

  // 일일 목표 달성 체크
  const checkDailyGoals = useCallback(() => {
    // 예시: 하루에 3번 이상 식사 기록시 성취
    const todayMeals = 3; // 실제로는 API에서 가져와야 함
    
    if (todayMeals >= 3) {
      triggerAchievement({
        id: 'daily_logger',
        type: 'milestone',
        title: '오늘의 기록왕',
        message: '하루 3번 이상 식사를 기록했습니다!',
        icon: '📝',
        points: 50,
        rarity: 'common'
      });
    }
  }, [triggerAchievement]);

  // 주간 목표 달성 체크
  const checkWeeklyGoals = useCallback((carbonSaved: number) => {
    if (carbonSaved >= 10) {
      triggerAchievement({
        id: 'weekly_saver',
        type: 'milestone',
        title: '주간 탄소 절약자',
        message: `이번 주 ${carbonSaved.toFixed(1)}kg의 탄소를 절약했습니다!`,
        icon: '🌱',
        points: 200,
        rarity: 'rare'
      });
    }
  }, [triggerAchievement]);

  // 연속 기록 체크
  const checkStreak = useCallback((streakDays: number) => {
    if (streakDays === 7) {
      triggerAchievement({
        id: 'week_streak',
        type: 'streak',
        title: '일주일 연속 기록',
        message: '7일 연속으로 식사를 기록했습니다!',
        icon: '🔥',
        points: 300,
        rarity: 'rare'
      });
    } else if (streakDays === 30) {
      triggerAchievement({
        id: 'month_streak',
        type: 'streak',
        title: '한달 연속 기록',
        message: '30일 연속 기록! 정말 대단해요!',
        icon: '🔥',
        points: 1000,
        rarity: 'epic'
      });
    } else if (streakDays === 100) {
      triggerAchievement({
        id: 'hundred_streak',
        type: 'streak',
        title: '백일 기록의 대가',
        message: '100일 연속 기록! 당신은 진정한 환경 지킴이입니다!',
        icon: '👑',
        points: 5000,
        rarity: 'legendary'
      });
    }
  }, [triggerAchievement]);

  // 스마트 스왑 성취 체크
  const checkSwapAchievements = useCallback((swapCount: number) => {
    if (swapCount === 1) {
      triggerAchievement({
        id: 'first_swap',
        type: 'milestone',
        title: '첫 번째 스마트 스왑',
        message: '지구를 위한 첫 번째 선택을 하셨군요!',
        icon: '🔄',
        points: 100,
        rarity: 'common'
      });
    } else if (swapCount === 10) {
      triggerAchievement({
        id: 'swap_enthusiast',
        type: 'milestone',
        title: '스왑 애호가',
        message: '10번의 스마트한 선택! 환경에 큰 도움이 되고 있어요',
        icon: '🌟',
        points: 500,
        rarity: 'rare'
      });
    } else if (swapCount === 50) {
      triggerAchievement({
        id: 'swap_master',
        type: 'milestone',
        title: '스왑 마스터',
        message: '50번의 스마트 스왑! 당신은 진정한 환경 마스터입니다',
        icon: '🏆',
        points: 2000,
        rarity: 'epic'
      });
    }
  }, [triggerAchievement]);

  // 레벨 시스템
  const getCurrentLevel = useCallback(() => {
    const points = state.totalPoints;
    if (points < 500) return { level: 1, title: '새싹 지킴이', next: 500 };
    if (points < 1500) return { level: 2, title: '친환경 실천가', next: 1500 };
    if (points < 3000) return { level: 3, title: '탄소 절약자', next: 3000 };
    if (points < 5000) return { level: 4, title: '환경 전문가', next: 5000 };
    if (points < 10000) return { level: 5, title: '지구 지킴이', next: 10000 };
    return { level: 6, title: '환경 마스터', next: null };
  }, [state.totalPoints]);

  // 동기부여 메시지 생성
  const getMotivationalMessage = useCallback(() => {
    const messages = [
      "오늘도 지구를 위한 작은 실천을 해보세요! 🌍",
      "당신의 선택이 지구의 미래를 바꿉니다! ✨",
      "작은 변화가 큰 차이를 만듭니다! 🌱",
      "오늘은 어떤 친환경 선택을 해보실까요? 🤔",
      "지속 가능한 미래는 우리가 만들어갑니다! 💚"
    ];
    return messages[Math.floor(Math.random() * messages.length)];
  }, []);

  return {
    // 상태
    ...state,
    currentLevel: getCurrentLevel(),
    
    // 액션
    triggerAchievement,
    updateProgress,
    checkDailyGoals,
    checkWeeklyGoals,
    checkStreak,
    checkSwapAchievements,
    
    // 유틸리티
    getMotivationalMessage
  };
};

// 헬퍼 함수
const getProgressIcon = (type: ProgressUpdate['type']): string => {
  const iconMap = {
    carbon_saved: '🌱',
    meal_logged: '🍽️',
    swap_accepted: '🔄',
    challenge_joined: '🎯',
    streak_extended: '🔥'
  };
  return iconMap[type] || '✅';
};

export default useGamification; 