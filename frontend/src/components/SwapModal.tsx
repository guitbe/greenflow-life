import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Check, ThumbsUp, ThumbsDown, ArrowRight } from 'lucide-react';
import toast from 'react-hot-toast';
import { SwapRecommendation } from '../types';
import { apiService } from '../services/api';

interface SwapModalProps {
  isOpen: boolean;
  onClose: () => void;
  recommendations: SwapRecommendation[];
  mealLogId: number;
  originalFood: string;
}

const SwapModal: React.FC<SwapModalProps> = ({ 
  isOpen, 
  onClose, 
  recommendations, 
  mealLogId, 
  originalFood 
}) => {
  const [selectedSwap, setSelectedSwap] = useState<SwapRecommendation | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAcceptSwap = async (recommendation: SwapRecommendation, accepted: boolean) => {
    try {
      setLoading(true);
      // In real implementation, you'd get the swap ID from the recommendation
      await apiService.acceptSwapRecommendation(mealLogId, accepted);
      
      if (accepted) {
        toast.success(`🌱 ${recommendation.recommended_food} 스왑을 선택했습니다!`);
      } else {
        toast.success('피드백이 저장되었습니다');
      }
      
      onClose();
    } catch (error) {
      toast.error('오류가 발생했습니다');
    } finally {
      setLoading(false);
    }
  };

  const getReductionColor = (percentage: number) => {
    if (percentage >= 70) return 'text-green-600 bg-green-100';
    if (percentage >= 40) return 'text-yellow-600 bg-yellow-100';
    return 'text-orange-600 bg-orange-100';
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="sticky top-0 bg-white border-b p-6 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-gray-800">
                  🔄 스마트 스왑 제안
                </h2>
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                <span className="font-medium">{originalFood}</span> 대신 이런 메뉴는 어떠세요?
              </p>
            </div>

            {/* Recommendations */}
            <div className="p-6 space-y-4">
              {recommendations.map((recommendation, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`border rounded-xl p-4 transition-all cursor-pointer ${
                    selectedSwap === recommendation 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-gray-200 hover:border-green-300 hover:bg-green-50'
                  }`}
                  onClick={() => setSelectedSwap(recommendation)}
                >
                  {/* Food Swap */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl">🍽️</div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-500 line-through">{recommendation.original_food}</span>
                          <ArrowRight className="w-4 h-4 text-gray-400" />
                          <span className="font-medium text-gray-800">{recommendation.recommended_food}</span>
                        </div>
                        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                          {recommendation.category}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Carbon Reduction */}
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm text-gray-600">탄소 절약량:</span>
                    <div className="text-right">
                      <div className="font-semibold text-gray-800">
                        {recommendation.carbon_reduction.toFixed(2)} kg CO₂e
                      </div>
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${getReductionColor(recommendation.carbon_reduction_percentage)}`}>
                        {recommendation.carbon_reduction_percentage.toFixed(0)}% 감소
                      </span>
                    </div>
                  </div>

                  {/* Message */}
                  <div className="bg-blue-50 rounded-lg p-3 mb-4">
                    <p className="text-sm text-blue-800">
                      {recommendation.recommendation_message}
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAcceptSwap(recommendation, true);
                      }}
                      disabled={loading}
                      className="flex-1 flex items-center justify-center px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 transition-colors text-sm font-medium"
                    >
                      <ThumbsUp className="w-4 h-4 mr-1" />
                      선택
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAcceptSwap(recommendation, false);
                      }}
                      disabled={loading}
                      className="flex-1 flex items-center justify-center px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:bg-gray-100 transition-colors text-sm font-medium"
                    >
                      <ThumbsDown className="w-4 h-4 mr-1" />
                      패스
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Footer */}
            <div className="border-t p-6">
              <div className="text-center">
                <p className="text-xs text-gray-500 mb-2">
                  💡 스마트 스왑으로 지구를 지키고 건강도 챙기세요!
                </p>
                <button
                  onClick={onClose}
                  className="text-sm text-gray-600 hover:text-gray-800 transition-colors"
                >
                  나중에 결정하기
                </button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default SwapModal; 