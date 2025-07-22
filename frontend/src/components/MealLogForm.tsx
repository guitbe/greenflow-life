import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { Camera, Plus, Calculator } from 'lucide-react';
import toast from 'react-hot-toast';
import { MealCreate, MealType, CarbonCalculationResponse } from '../types';
import { apiService } from '../services/api';

interface MealLogFormProps {
  onMealLogged?: (meal: any) => void;
}

interface FormData {
  food_name: string;
  portion_size: number;
  meal_type: MealType;
  image_url?: string;
}

const MealLogForm: React.FC<MealLogFormProps> = ({ onMealLogged }) => {
  const [loading, setLoading] = useState(false);
  const [carbonData, setCarbonData] = useState<CarbonCalculationResponse | null>(null);
  const [calculating, setCalculating] = useState(false);

  const { register, handleSubmit, watch, setValue, reset, formState: { errors } } = useForm<FormData>();

  const watchedFoodName = watch('food_name');
  const watchedPortionSize = watch('portion_size');

  const calculateCarbon = async () => {
    if (!watchedFoodName || !watchedPortionSize) {
      toast.error('음식명과 양을 모두 입력해주세요');
      return;
    }

    try {
      setCalculating(true);
      const result = await apiService.calculateCarbonFootprint({
        food_name: watchedFoodName,
        portion_size: watchedPortionSize
      });
      setCarbonData(result);
      toast.success('탄소 발자국이 계산되었습니다!');
    } catch (error) {
      toast.error('탄소 발자국 계산에 실패했습니다');
    } finally {
      setCalculating(false);
    }
  };

  const onSubmit = async (data: FormData) => {
    try {
      setLoading(true);
      const mealLog = await apiService.createMealLog(data);
      toast.success('식사가 성공적으로 기록되었습니다! 🍽️');
      reset();
      setCarbonData(null);
      onMealLogged?.(mealLog);
    } catch (error) {
      toast.error('식사 기록에 실패했습니다');
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // TODO: Implement Cloudinary upload
      const imageUrl = URL.createObjectURL(file);
      setValue('image_url', imageUrl);
      toast.success('이미지가 업로드되었습니다!');
    }
  };

  const getSustainabilityColor = (rating: string) => {
    switch (rating) {
      case 'HIGH': return 'text-green-600 bg-green-100';
      case 'MEDIUM': return 'text-yellow-600 bg-yellow-100';
      case 'LOW': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getSustainabilityText = (rating: string) => {
    switch (rating) {
      case 'HIGH': return '친환경';
      case 'MEDIUM': return '보통';
      case 'LOW': return '주의';
      default: return '알 수 없음';
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-lg p-6 max-w-md mx-auto"
    >
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        🍽️ 오늘의 식사 기록
      </h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Food Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            음식명 *
          </label>
          <input
            {...register('food_name', { required: '음식명을 입력해주세요' })}
            type="text"
            placeholder="예: 소고기 불고기"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
          {errors.food_name && (
            <p className="mt-1 text-sm text-red-600">{errors.food_name.message}</p>
          )}
        </div>

        {/* Portion Size */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            양 (그램) *
          </label>
          <input
            {...register('portion_size', { 
              required: '양을 입력해주세요',
              min: { value: 1, message: '1g 이상 입력해주세요' }
            })}
            type="number"
            placeholder="예: 200"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
          {errors.portion_size && (
            <p className="mt-1 text-sm text-red-600">{errors.portion_size.message}</p>
          )}
        </div>

        {/* Meal Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            식사 종류 *
          </label>
          <select
            {...register('meal_type', { required: '식사 종류를 선택해주세요' })}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="">선택해주세요</option>
            <option value="breakfast">아침</option>
            <option value="lunch">점심</option>
            <option value="dinner">저녁</option>
            <option value="snack">간식</option>
          </select>
          {errors.meal_type && (
            <p className="mt-1 text-sm text-red-600">{errors.meal_type.message}</p>
          )}
        </div>

        {/* Image Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            사진 (선택사항)
          </label>
          <div className="flex items-center justify-center w-full">
            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <Camera className="w-8 h-8 mb-2 text-gray-400" />
                <p className="text-sm text-gray-500">사진을 업로드하세요</p>
              </div>
              <input 
                type="file" 
                accept="image/*" 
                className="hidden" 
                onChange={handleImageUpload}
              />
            </label>
          </div>
        </div>

        {/* Carbon Calculation */}
        <div className="border-t pt-4">
          <button
            type="button"
            onClick={calculateCarbon}
            disabled={calculating || !watchedFoodName || !watchedPortionSize}
            className="w-full mb-4 flex items-center justify-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            <Calculator className="w-4 h-4 mr-2" />
            {calculating ? '계산 중...' : '탄소 발자국 계산'}
          </button>

          {carbonData && (
            <motion.div 
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="bg-gray-50 rounded-lg p-4 space-y-2"
            >
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">탄소 발자국:</span>
                <span className="font-semibold text-gray-800">
                  {carbonData.carbon_footprint.toFixed(2)} kg CO₂e
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">카테고리:</span>
                <span className="text-sm font-medium">{carbonData.category}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">지속가능성:</span>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${getSustainabilityColor(carbonData.sustainability_rating)}`}>
                  {getSustainabilityText(carbonData.sustainability_rating)}
                </span>
              </div>
            </motion.div>
          )}
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full flex items-center justify-center px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
        >
          <Plus className="w-4 h-4 mr-2" />
          {loading ? '기록 중...' : '식사 기록하기'}
        </button>
      </form>
    </motion.div>
  );
};

export default MealLogForm; 