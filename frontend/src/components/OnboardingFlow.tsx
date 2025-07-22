import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, Target, Utensils, ArrowRight, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';

interface OnboardingFlowProps {
  onComplete: (userData: OnboardingData) => void;
}

interface OnboardingData {
  name: string;
  monthlyGoal: string;
  dietaryPreferences: string[];
  motivations: string[];
}

interface WelcomeScreenProps {
  onNext: (name: string) => void;
}

interface GoalSettingScreenProps {
  name: string;
  onNext: (goal: string) => void;
  onPrev: () => void;
}

interface DietaryPreferenceScreenProps {
  name: string;
  goal: string;
  onComplete: (preferences: string[], motivations: string[]) => void;
  onPrev: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onNext }) => {
  const [name, setName] = useState('');

  const handleNext = () => {
    if (name.trim()) {
      onNext(name.trim());
    } else {
      toast.error('이름을 입력해주세요! 😊');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -50 }}
      className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: "spring" }}
        className="mb-8"
      >
        <div className="w-24 h-24 bg-green-500 rounded-full flex items-center justify-center text-white text-4xl">
          🌱
        </div>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="text-4xl font-bold text-gray-800 mb-4 text-center"
      >
        Greenflow Life에 
        <br />
        <span className="text-green-600">오신 것을 환영해요!</span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="text-lg text-gray-600 mb-8 text-center max-w-md"
      >
        맛있는 음식과 함께 지구를 지키는 여정을 시작해보세요. 
        작은 선택이 큰 변화를 만듭니다! 🌍
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="w-full max-w-md"
      >
        <input
          type="text"
          placeholder="이름을 알려주세요"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleNext()}
          className="w-full px-6 py-4 rounded-xl border-2 border-gray-200 focus:border-green-500 focus:outline-none text-lg text-center"
        />
        
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleNext}
          className="w-full mt-6 bg-green-500 hover:bg-green-600 text-white font-semibold py-4 px-6 rounded-xl flex items-center justify-center gap-2 transition-colors"
        >
          시작하기 <ArrowRight className="w-5 h-5" />
        </motion.button>
      </motion.div>
    </motion.div>
  );
};

const GoalSettingScreen: React.FC<GoalSettingScreenProps> = ({ name, onNext, onPrev }) => {
  const [selectedGoal, setSelectedGoal] = useState<string>('');

  const goals = [
    {
      id: 'beginner',
      title: '🌱 지구 친화적 시작',
      description: '탄소 발자국을 줄이는 첫 걸음',
      target: '월 10% 탄소 절약'
    },
    {
      id: 'intermediate',
      title: '🌿 의식적인 소비자',
      description: '꾸준한 친환경 식단 실천',
      target: '월 25% 탄소 절약'
    },
    {
      id: 'advanced',
      title: '🌳 지구 지킴이',
      description: '적극적인 환경 보호 실천',
      target: '월 40% 탄소 절약'
    }
  ];

  const handleNext = () => {
    if (selectedGoal) {
      onNext(selectedGoal);
    } else {
      toast.error('목표를 선택해주세요! 🎯');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6"
    >
      <motion.h2
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-3xl font-bold text-gray-800 mb-2 text-center"
      >
        안녕하세요, {name}님! 👋
      </motion.h2>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="text-lg text-gray-600 mb-8 text-center max-w-md"
      >
        어떤 목표로 시작해보고 싶으신가요?
      </motion.p>

      <div className="w-full max-w-md space-y-4">
        {goals.map((goal, index) => (
          <motion.button
            key={goal.id}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setSelectedGoal(goal.id)}
            className={`w-full p-6 rounded-xl border-2 text-left transition-all ${
              selectedGoal === goal.id
                ? 'border-green-500 bg-green-50 shadow-md'
                : 'border-gray-200 bg-white hover:border-green-300'
            }`}
          >
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl">{goal.title.split(' ')[0]}</span>
              <h3 className="font-semibold text-gray-800">{goal.title.substring(3)}</h3>
            </div>
            <p className="text-gray-600 text-sm mb-2">{goal.description}</p>
            <div className="flex items-center gap-2">
              <Target className="w-4 h-4 text-green-500" />
              <span className="text-green-600 font-medium text-sm">{goal.target}</span>
            </div>
          </motion.button>
        ))}
      </div>

      <div className="flex gap-4 mt-8 w-full max-w-md">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onPrev}
          className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-6 rounded-xl transition-colors"
        >
          이전
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleNext}
          className="flex-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition-colors"
        >
          다음 <ArrowRight className="w-5 h-5" />
        </motion.button>
      </div>
    </motion.div>
  );
};

const DietaryPreferenceScreen: React.FC<DietaryPreferenceScreenProps> = ({ 
  name, 
  goal, 
  onComplete, 
  onPrev 
}) => {
  const [selectedPreferences, setSelectedPreferences] = useState<string[]>([]);
  const [selectedMotivations, setSelectedMotivations] = useState<string[]>([]);

  const preferences = [
    { id: 'omnivore', label: '🍖 잡식 (모든 음식)', icon: '🍽️' },
    { id: 'reduce_meat', label: '🥗 육류 줄이는 중', icon: '📉' },
    { id: 'pescatarian', label: '🐟 페스코 베지테리안', icon: '🐠' },
    { id: 'vegetarian', label: '🥕 베지테리안', icon: '🌱' },
    { id: 'vegan', label: '🌿 비건', icon: '💚' }
  ];

  const motivations = [
    { id: 'environment', label: '🌍 환경 보호', desc: '지구를 위한 선택' },
    { id: 'health', label: '💪 건강 관리', desc: '더 건강한 나를 위해' },
    { id: 'cost', label: '💰 경제적 이유', desc: '가계부를 생각하며' },
    { id: 'curiosity', label: '🤔 호기심', desc: '새로운 도전을 위해' }
  ];

  const togglePreference = (pref: string) => {
    setSelectedPreferences(prev => 
      prev.includes(pref) 
        ? prev.filter(p => p !== pref)
        : [...prev, pref]
    );
  };

  const toggleMotivation = (motivation: string) => {
    setSelectedMotivations(prev => 
      prev.includes(motivation)
        ? prev.filter(m => m !== motivation)
        : [...prev, motivation]
    );
  };

  const handleComplete = () => {
    if (selectedPreferences.length === 0) {
      toast.error('식단 선호도를 선택해주세요! 🍽️');
      return;
    }
    if (selectedMotivations.length === 0) {
      toast.error('동기를 선택해주세요! 💪');
      return;
    }
    
    onComplete(selectedPreferences, selectedMotivations);
    toast.success('환영합니다! 함께 지구를 지켜요! 🌍✨');
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6"
    >
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          마지막 단계예요! 🎯
        </h2>
        <p className="text-lg text-gray-600">
          {name}님의 식단과 동기를 알려주세요
        </p>
      </motion.div>

      <div className="w-full max-w-md space-y-8">
        {/* 식단 선호도 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Utensils className="w-5 h-5" />
            식단 선호도
          </h3>
          <div className="space-y-3">
            {preferences.map((pref, index) => (
              <motion.button
                key={pref.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => togglePreference(pref.id)}
                className={`w-full p-4 rounded-lg border-2 text-left transition-all ${
                  selectedPreferences.includes(pref.id)
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 bg-white hover:border-green-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{pref.icon}</span>
                  <span className="font-medium">{pref.label}</span>
                  {selectedPreferences.includes(pref.id) && (
                    <CheckCircle className="w-5 h-5 text-green-500 ml-auto" />
                  )}
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>

        {/* 동기 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Sparkles className="w-5 h-5" />
            동기 (복수 선택 가능)
          </h3>
          <div className="space-y-3">
            {motivations.map((motivation, index) => (
              <motion.button
                key={motivation.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => toggleMotivation(motivation.id)}
                className={`w-full p-4 rounded-lg border-2 text-left transition-all ${
                  selectedMotivations.includes(motivation.id)
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 bg-white hover:border-green-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div>
                    <div className="font-medium">{motivation.label}</div>
                    <div className="text-sm text-gray-500">{motivation.desc}</div>
                  </div>
                  {selectedMotivations.includes(motivation.id) && (
                    <CheckCircle className="w-5 h-5 text-green-500 ml-auto" />
                  )}
                </div>
              </motion.button>
            ))}
          </div>
        </motion.div>
      </div>

      <div className="flex gap-4 mt-8 w-full max-w-md">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onPrev}
          className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-6 rounded-xl transition-colors"
        >
          이전
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleComplete}
          className="flex-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition-colors"
        >
          완료! <Sparkles className="w-5 h-5" />
        </motion.button>
      </div>
    </motion.div>
  );
};

export const OnboardingFlow: React.FC<OnboardingFlowProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [userData, setUserData] = useState<Partial<OnboardingData>>({});

  const handleWelcomeNext = (name: string) => {
    setUserData(prev => ({ ...prev, name }));
    setCurrentStep(2);
  };

  const handleGoalNext = (goal: string) => {
    setUserData(prev => ({ ...prev, monthlyGoal: goal }));
    setCurrentStep(3);
  };

  const handleComplete = (preferences: string[], motivations: string[]) => {
    const finalData: OnboardingData = {
      name: userData.name!,
      monthlyGoal: userData.monthlyGoal!,
      dietaryPreferences: preferences,
      motivations: motivations
    };
    onComplete(finalData);
  };

  return (
    <div className="relative overflow-hidden">
      <AnimatePresence mode="wait">
        {currentStep === 1 && (
          <WelcomeScreen key="welcome" onNext={handleWelcomeNext} />
        )}
        {currentStep === 2 && (
          <GoalSettingScreen 
            key="goal"
            name={userData.name!}
            onNext={handleGoalNext}
            onPrev={() => setCurrentStep(1)}
          />
        )}
        {currentStep === 3 && (
          <DietaryPreferenceScreen
            key="preferences"
            name={userData.name!}
            goal={userData.monthlyGoal!}
            onComplete={handleComplete}
            onPrev={() => setCurrentStep(2)}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default OnboardingFlow; 