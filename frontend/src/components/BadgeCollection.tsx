import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Trophy, Lock, Star, Calendar, Users, Target, Award } from 'lucide-react';
import { Badge, UserBadge } from '../types';
import { apiService } from '../services/api';
import toast from 'react-hot-toast';

interface BadgeCollectionProps {
  className?: string;
}

interface BadgeCategory {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
}

const badgeCategories: BadgeCategory[] = [
  { id: 'all', name: '전체', icon: Trophy, color: 'text-yellow-500' },
  { id: 'milestones', name: '마일스톤', icon: Target, color: 'text-blue-500' },
  { id: 'streaks', name: '연속 달성', icon: Calendar, color: 'text-green-500' },
  { id: 'achievements', name: '특별 성취', icon: Star, color: 'text-purple-500' },
  { id: 'social', name: '소셜', icon: Users, color: 'text-pink-500' }
];

const getBadgeIcon = (badgeType: string): string => {
  const iconMap: { [key: string]: string } = {
    'first_meal': '🍽️',
    'first_swap': '🔄',
    'week_streak': '📅',
    'month_streak': '🗓️',
    'carbon_saver': '🌱',
    'eco_warrior': '🌍',
    'challenge_master': '🏆',
    'social_sharer': '📢',
    'data_enthusiast': '📊',
    'consistency_king': '👑',
    'green_pioneer': '🌿',
    'impact_maker': '⭐'
  };
  return iconMap[badgeType] || '🏅';
};

const getBadgeRarity = (badgeType: string): { rarity: string; color: string; glow: string } => {
  const rarityMap: { [key: string]: { rarity: string; color: string; glow: string } } = {
    'first_meal': { rarity: 'Common', color: 'border-gray-300 bg-gray-50', glow: 'shadow-gray-200' },
    'first_swap': { rarity: 'Common', color: 'border-green-300 bg-green-50', glow: 'shadow-green-200' },
    'week_streak': { rarity: 'Rare', color: 'border-blue-300 bg-blue-50', glow: 'shadow-blue-200' },
    'month_streak': { rarity: 'Epic', color: 'border-purple-300 bg-purple-50', glow: 'shadow-purple-200' },
    'carbon_saver': { rarity: 'Rare', color: 'border-green-400 bg-green-100', glow: 'shadow-green-300' },
    'eco_warrior': { rarity: 'Legendary', color: 'border-yellow-400 bg-yellow-50', glow: 'shadow-yellow-300' },
    'challenge_master': { rarity: 'Epic', color: 'border-purple-400 bg-purple-100', glow: 'shadow-purple-300' },
    'social_sharer': { rarity: 'Common', color: 'border-pink-300 bg-pink-50', glow: 'shadow-pink-200' },
    'data_enthusiast': { rarity: 'Rare', color: 'border-indigo-300 bg-indigo-50', glow: 'shadow-indigo-200' },
    'consistency_king': { rarity: 'Epic', color: 'border-orange-400 bg-orange-100', glow: 'shadow-orange-300' },
    'green_pioneer': { rarity: 'Legendary', color: 'border-emerald-400 bg-emerald-100', glow: 'shadow-emerald-300' },
    'impact_maker': { rarity: 'Legendary', color: 'border-yellow-500 bg-yellow-100', glow: 'shadow-yellow-400' }
  };
  return rarityMap[badgeType] || { rarity: 'Common', color: 'border-gray-300 bg-gray-50', glow: 'shadow-gray-200' };
};

export const BadgeCollection: React.FC<BadgeCollectionProps> = ({ className = '' }) => {
  const [badges, setBadges] = useState<Badge[]>([]);
  const [userBadges, setUserBadges] = useState<UserBadge[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedBadge, setSelectedBadge] = useState<Badge | null>(null);

  useEffect(() => {
    fetchBadgeData();
  }, []);

  const fetchBadgeData = async () => {
    try {
      const [badgesResponse, userBadgesResponse] = await Promise.all([
        apiService.get('/api/challenges/badges'),
        apiService.get('/api/challenges/my-badges')
      ]);
      
      setBadges(badgesResponse.data || []);
      setUserBadges(userBadgesResponse.data || []);
    } catch (error) {
      console.error('Failed to fetch badge data:', error);
      toast.error('배지 정보를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const getEarnedBadge = (badgeId: number): UserBadge | undefined => {
    return userBadges.find(ub => ub.badge.id === badgeId);
  };

  const isEarned = (badgeId: number): boolean => {
    return !!getEarnedBadge(badgeId);
  };

  const filteredBadges = badges.filter(badge => {
    if (selectedCategory === 'all') return true;
    return badge.category === selectedCategory;
  });

  const earnedCount = badges.filter(badge => isEarned(badge.id)).length;
  const completionPercentage = badges.length > 0 ? Math.round((earnedCount / badges.length) * 100) : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 ${className}`}>
      {/* 헤더 */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-4">
          <Trophy className="w-8 h-8 text-yellow-500" />
          <div>
            <h2 className="text-2xl font-bold text-gray-800">배지 컬렉션</h2>
            <p className="text-gray-600">
              {earnedCount}/{badges.length} 개 획득 ({completionPercentage}% 완료)
            </p>
          </div>
        </div>

        {/* 진행률 바 */}
        <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${completionPercentage}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full relative"
          >
            <div className="absolute inset-0 bg-white opacity-30 rounded-full animate-pulse"></div>
          </motion.div>
        </div>
      </div>

      {/* 카테고리 필터 */}
      <div className="flex gap-2 mb-6 overflow-x-auto">
        {badgeCategories.map(category => {
          const Icon = category.icon;
          return (
            <motion.button
              key={category.id}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg whitespace-nowrap transition-all ${
                selectedCategory === category.id
                  ? 'bg-green-500 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="text-sm font-medium">{category.name}</span>
            </motion.button>
          );
        })}
      </div>

      {/* 배지 그리드 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <AnimatePresence>
          {filteredBadges.map((badge, index) => {
            const earned = isEarned(badge.id);
            const userBadge = getEarnedBadge(badge.id);
            const badgeRarity = getBadgeRarity(badge.badge_type);
            const badgeIcon = getBadgeIcon(badge.badge_type);

            return (
              <motion.div
                key={badge.id}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: earned ? 1.05 : 0.95, y: earned ? -5 : 0 }}
                onClick={() => setSelectedBadge(badge)}
                className={`relative p-4 rounded-xl border-2 cursor-pointer transition-all ${
                  earned 
                    ? `${badgeRarity.color} ${badgeRarity.glow} shadow-lg` 
                    : 'border-gray-200 bg-gray-50 opacity-60'
                }`}
              >
                {/* 배지 아이콘 */}
                <div className="relative mb-3">
                  <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center text-3xl ${
                    earned ? 'bg-white shadow-md' : 'bg-gray-200'
                  }`}>
                    {earned ? badgeIcon : '🔒'}
                  </div>
                  
                  {/* 등급 표시 */}
                  {earned && (
                    <div className="absolute -top-1 -right-1">
                      <div className={`px-2 py-1 rounded-full text-xs font-bold ${
                        badgeRarity.rarity === 'Legendary' ? 'bg-yellow-400 text-yellow-900' :
                        badgeRarity.rarity === 'Epic' ? 'bg-purple-400 text-purple-900' :
                        badgeRarity.rarity === 'Rare' ? 'bg-blue-400 text-blue-900' :
                        'bg-gray-400 text-gray-900'
                      }`}>
                        {badgeRarity.rarity}
                      </div>
                    </div>
                  )}

                  {/* 잠금 아이콘 */}
                  {!earned && (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Lock className="w-6 h-6 text-gray-400" />
                    </div>
                  )}
                </div>

                {/* 배지 정보 */}
                <div className="text-center">
                  <h3 className={`font-semibold text-sm mb-1 ${earned ? 'text-gray-800' : 'text-gray-500'}`}>
                    {badge.name}
                  </h3>
                  <p className={`text-xs ${earned ? 'text-gray-600' : 'text-gray-400'}`}>
                    {badge.description}
                  </p>
                  
                  {/* 획득 날짜 */}
                  {earned && userBadge && (
                    <p className="text-xs text-green-600 font-medium mt-2">
                      {new Date(userBadge.earned_at).toLocaleDateString('ko-KR')} 획득
                    </p>
                  )}
                </div>

                {/* 반짝이는 효과 (획득한 배지) */}
                {earned && (
                  <motion.div
                    animate={{ 
                      opacity: [0, 1, 0],
                      scale: [1, 1.2, 1]
                    }}
                    transition={{ 
                      duration: 2,
                      repeat: Infinity,
                      repeatDelay: 3
                    }}
                    className="absolute top-2 right-2"
                  >
                    <Star className="w-4 h-4 text-yellow-400" />
                  </motion.div>
                )}
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* 빈 상태 */}
      {filteredBadges.length === 0 && (
        <div className="text-center py-12">
          <Trophy className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-500 mb-2">
            아직 이 카테고리에 배지가 없어요
          </h3>
          <p className="text-gray-400">
            다른 카테고리를 확인해보세요!
          </p>
        </div>
      )}

      {/* 배지 상세 모달 */}
      <AnimatePresence>
        {selectedBadge && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
            onClick={() => setSelectedBadge(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl"
            >
              <div className="text-center">
                <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center text-4xl">
                  {getBadgeIcon(selectedBadge.badge_type)}
                </div>
                
                <h3 className="text-2xl font-bold text-gray-800 mb-2">
                  {selectedBadge.name}
                </h3>
                
                <p className="text-gray-600 mb-4">
                  {selectedBadge.description}
                </p>

                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <h4 className="font-semibold text-gray-800 mb-2">획득 조건</h4>
                  <p className="text-sm text-gray-600">
                    {selectedBadge.criteria || '특정 조건을 달성하면 획득할 수 있습니다.'}
                  </p>
                </div>

                {isEarned(selectedBadge.id) ? (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-center justify-center gap-2 text-green-700">
                      <Award className="w-5 h-5" />
                      <span className="font-semibold">획득 완료!</span>
                    </div>
                    <p className="text-green-600 text-sm mt-2">
                      {new Date(getEarnedBadge(selectedBadge.id)!.earned_at).toLocaleDateString('ko-KR')}에 획득
                    </p>
                  </div>
                ) : (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="flex items-center justify-center gap-2 text-yellow-700">
                      <Target className="w-5 h-5" />
                      <span className="font-semibold">도전해보세요!</span>
                    </div>
                    <p className="text-yellow-600 text-sm mt-2">
                      조건을 달성하면 이 멋진 배지를 얻을 수 있어요
                    </p>
                  </div>
                )}

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedBadge(null)}
                  className="mt-6 w-full bg-gray-500 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
                >
                  닫기
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default BadgeCollection; 