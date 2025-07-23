import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line
} from 'recharts';
import { 
  Leaf, 
  TrendingDown, 
  Target, 
  Award,
  Calendar,
  Zap
} from 'lucide-react';
import { DashboardData } from '../types';
import { apiService } from '../services/api';
import InsightCard from './InsightCard';

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async (isRetry: boolean = false) => {
    try {
      if (!isRetry) {
        setLoading(true);
        setError(null);
      }
      
      const data = await apiService.getDashboardData();
      setDashboardData(data);
      setRetryCount(0); // Reset retry count on success
    } catch (err: any) {
      console.error('Dashboard data fetch error:', err);
      
      // Handle different types of errors
      let errorMessage = '대시보드 데이터를 불러오는 데 실패했습니다.';
      
      if (err?.response?.status === 401 || err?.response?.status === 403) {
        errorMessage = '인증이 필요합니다. 다시 로그인해주세요.';
      } else if (err?.response?.status === 500) {
        errorMessage = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
      } else if (err?.code === 'NETWORK_ERROR' || !navigator.onLine) {
        errorMessage = '네트워크 연결을 확인해주세요.';
      }
      
      setError(errorMessage);
      
      // Auto-retry up to 3 times for network/server errors
      if (retryCount < 3 && (err?.response?.status >= 500 || err?.code === 'NETWORK_ERROR')) {
        setTimeout(() => {
          console.log(`Retrying dashboard fetch... (attempt ${retryCount + 1})`);
          setRetryCount(prev => prev + 1);
          fetchDashboardData(true);
        }, 2000 * (retryCount + 1)); // Exponential backoff
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-500"></div>
      </div>
    );
  }

  if (error || !dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <button 
            onClick={() => fetchDashboardData(false)}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  const { stats, carbon_trends, top_contributors, insights } = dashboardData;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            안녕하세요! 오늘도 지구를 지켜봐요 🌍
          </h1>
          <p className="text-gray-600">
            이번 주 탄소 절약량과 활동을 확인해보세요
          </p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="이번 주 탄소 배출"
            value={`${stats.total_carbon_this_week.toFixed(1)}kg`}
            icon={<Leaf className="w-6 h-6" />}
            color="green"
            subtitle="CO₂e"
          />
          <StatCard
            title="탄소 절약량"
            value={`${stats.carbon_reduction_achieved.toFixed(1)}kg`}
            icon={<TrendingDown className="w-6 h-6" />}
            color="blue"
            subtitle="스마트 스왑으로"
          />
          <StatCard
            title="목표 달성률"
            value={`${stats.target_progress_percentage.toFixed(0)}%`}
            icon={<Target className="w-6 h-6" />}
            color="purple"
            subtitle="이번 달"
          />
          <StatCard
            title="활성 챌린지"
            value={stats.active_challenges.toString()}
            icon={<Award className="w-6 h-6" />}
            color="orange"
            subtitle="참여 중"
          />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Carbon Trend Chart */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <Calendar className="w-5 h-5 mr-2 text-green-500" />
              주간 탄소 발자국 트렌드
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={carbon_trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => {
                    const date = new Date(value);
                    return `${date.getMonth() + 1}/${date.getDate()}`;
                  }}
                />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip 
                  labelFormatter={(value) => `날짜: ${value}`}
                  formatter={(value: number) => [`${value.toFixed(2)}kg CO₂e`, '탄소 배출량']}
                />
                <Line 
                  type="monotone" 
                  dataKey="carbon_amount" 
                  stroke="#10b981" 
                  strokeWidth={3}
                  dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </motion.div>

          {/* Top Contributors */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
              <Zap className="w-5 h-5 mr-2 text-orange-500" />
              탄소 배출 상위 음식
            </h3>
            <div className="space-y-4">
              {top_contributors.slice(0, 5).map((contributor, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white ${
                      index === 0 ? 'bg-red-500' : 
                      index === 1 ? 'bg-orange-500' : 
                      index === 2 ? 'bg-yellow-500' : 'bg-gray-400'
                    }`}>
                      {index + 1}
                    </div>
                    <div className="ml-3">
                      <p className="font-medium text-gray-800">{contributor.food_name}</p>
                      <p className="text-sm text-gray-600">{contributor.frequency}회 섭취</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-gray-800">{contributor.total_carbon.toFixed(1)}kg</p>
                    <p className="text-sm text-gray-600">CO₂e</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Insights Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-6">개인화된 인사이트</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {insights.map((insight, index) => (
              <InsightCard key={index} insight={insight} />
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

interface StatCardProps {
  title: string;
  value: string;
  icon: React.ReactNode;
  color: 'green' | 'blue' | 'purple' | 'orange';
  subtitle: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, color, subtitle }) => {
  const colorClasses = {
    green: 'bg-green-500',
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500'
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`${colorClasses[color]} text-white p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
      <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
      <p className="text-sm text-gray-500">{subtitle}</p>
    </motion.div>
  );
};

export default Dashboard; 