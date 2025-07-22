import React from 'react';
import { motion } from 'framer-motion';
import { InsightCard as InsightCardType } from '../types';

interface InsightCardProps {
  insight: InsightCardType;
}

const InsightCard: React.FC<InsightCardProps> = ({ insight }) => {
  const getCardStyles = (type: string) => {
    switch (type) {
      case 'achievement':
        return 'bg-gradient-to-br from-green-50 to-green-100 border-green-200';
      case 'tip':
        return 'bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200';
      case 'warning':
        return 'bg-gradient-to-br from-red-50 to-red-100 border-red-200';
      case 'celebration':
        return 'bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200';
      default:
        return 'bg-gradient-to-br from-gray-50 to-gray-100 border-gray-200';
    }
  };

  const getIconStyles = (type: string) => {
    switch (type) {
      case 'achievement':
        return 'text-green-600';
      case 'tip':
        return 'text-blue-600';
      case 'warning':
        return 'text-red-600';
      case 'celebration':
        return 'text-purple-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className={`rounded-xl border p-6 hover:shadow-lg transition-all ${getCardStyles(insight.type)}`}
    >
      <div className="flex items-start space-x-4">
        <div className={`text-2xl ${getIconStyles(insight.type)}`}>
          {insight.icon}
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-gray-800 mb-2">
            {insight.title}
          </h3>
          <p className="text-gray-600 text-sm mb-4">
            {insight.message}
          </p>
          <button className={`text-sm font-medium hover:underline ${getIconStyles(insight.type)}`}>
            {insight.action_text}
          </button>
        </div>
      </div>
    </motion.div>
  );
};

export default InsightCard; 