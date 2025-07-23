import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Components
import Dashboard from './components/Dashboard';
import OnboardingFlow from './components/OnboardingFlow';
import MealLogForm from './components/MealLogForm';
import BadgeCollection from './components/BadgeCollection';
import SwapModal from './components/SwapModal';

// Services
import { apiService } from './services/api';

// Types
import { User } from './types';

interface OnboardingData {
  name: string;
  monthlyGoal: string;
  dietaryPreferences: string[];
  motivations: string[];
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showMealForm, setShowMealForm] = useState(false);
  const [showSwapModal, setShowSwapModal] = useState(false);
  const [selectedMealId, setSelectedMealId] = useState<number>(0);
  const [originalFood, setOriginalFood] = useState<string>('');

  // Check if user is logged in on app start
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const userData = await apiService.getCurrentUser();
          setUser(userData);
        } catch (error) {
          localStorage.removeItem('access_token');
        }
      }
      setIsLoading(false);
    };
    
    checkAuth();
  }, []);

  const handleOnboardingComplete = async (onboardingData: OnboardingData) => {
    // Map dietary preferences to valid type
    const getDietaryPreference = (preferences: string[]): 'omnivore' | 'vegetarian' | 'vegan' | 'pescatarian' => {
      const validPreferences = ['omnivore', 'vegetarian', 'vegan', 'pescatarian'] as const;
      const firstPreference = preferences[0]?.toLowerCase();
      return validPreferences.includes(firstPreference as any) ? firstPreference as any : 'omnivore';
    };

    try {
      // Generate unique email with timestamp to avoid duplicates
      const timestamp = Date.now();
      const uniqueEmail = `${onboardingData.name.toLowerCase().replace(/\s+/g, '')}.${timestamp}@greenflow.temp`;

      // Register user with onboarding data
      await apiService.register({
        email: uniqueEmail,
        password: `temp123_${timestamp}`, // Make password unique as well
        name: onboardingData.name,
        dietary_preference: getDietaryPreference(onboardingData.dietaryPreferences)
      });
      
      // Get user data
      const userData = await apiService.getCurrentUser();
      setUser(userData);
    } catch (error: any) {
      console.error('Registration failed:', error);
      
      // Show more specific error message
      let errorMessage = '회원가입에 실패했습니다.';
      if (error?.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error?.message) {
        errorMessage = error.message;
      }
      
      // For demo purposes, still create a mock user but show the error
      alert(`⚠️ ${errorMessage}\n\n데모 모드로 계속 진행합니다.`);
      
      setUser({
        id: Date.now(), // Use timestamp as unique ID
        email: `${onboardingData.name.toLowerCase()}@demo.com`,
        name: onboardingData.name,
        dietary_preference: getDietaryPreference(onboardingData.dietaryPreferences),
        target_carbon_reduction: 20
      });
    }
  };

  const handleLogout = () => {
    apiService.logout();
    setUser(null);
  };



  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Greenflow Life 로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        {/* Navigation Header */}
        {user && (
          <nav className="bg-white shadow-sm border-b border-green-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between items-center h-16">
                <div className="flex items-center">
                  <h1 className="text-xl font-bold text-green-800">
                    🌱 Greenflow Life
                  </h1>
                </div>
                <div className="flex items-center space-x-4">
                  <span className="text-gray-700">안녕하세요, {user.name}님!</span>
                  <button
                    onClick={() => setShowMealForm(true)}
                    className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                  >
                    + 식사 추가
                  </button>
                  <button
                    onClick={handleLogout}
                    className="text-gray-500 hover:text-gray-700 text-sm"
                  >
                    로그아웃
                  </button>
                </div>
              </div>
            </div>
          </nav>
        )}

        <Routes>
          {/* Authentication Route */}
          <Route 
            path="/onboarding" 
            element={
              user ? <Navigate to="/dashboard" /> : <OnboardingFlow onComplete={handleOnboardingComplete} />
            } 
          />
          
          {/* Main Dashboard */}
          <Route 
            path="/dashboard" 
            element={
              user ? <Dashboard /> : <Navigate to="/onboarding" />
            } 
          />

          {/* Badges Page */}
          <Route 
            path="/badges" 
            element={
              user ? <BadgeCollection /> : <Navigate to="/onboarding" />
            } 
          />

          {/* Default Route */}
          <Route 
            path="/" 
            element={
              user ? <Navigate to="/dashboard" /> : <Navigate to="/onboarding" />
            } 
          />
        </Routes>

        {/* Meal Log Modal */}
        {showMealForm && user && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-bold text-gray-900">식사 기록 추가</h2>
                  <button
                    onClick={() => setShowMealForm(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>
                <MealLogForm 
                  onMealLogged={(meal) => {
                    setShowMealForm(false);
                    // Refresh page to show updated data
                    window.location.reload();
                  }}
                />
              </div>
            </div>
          </div>
        )}

        {/* Swap Modal */}
        <SwapModal
          isOpen={showSwapModal}
          onClose={() => {
            setShowSwapModal(false);
            setSelectedMealId(0);
            setOriginalFood('');
          }}
          recommendations={[]}
          mealLogId={selectedMealId}
          originalFood={originalFood}
        />

        {/* Quick Access Footer */}
        {user && (
          <div className="fixed bottom-6 right-6">
            <div className="flex flex-col space-y-2">
              <button
                onClick={() => setShowMealForm(true)}
                className="bg-green-500 hover:bg-green-600 text-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
                title="식사 추가"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
              </button>
              <a
                href="/badges"
                className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
                title="배지 확인"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </a>
            </div>
          </div>
        )}

        {/* Welcome Message for New Users */}
        {!user && (
          <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-green-800 mb-4">
                🌱 Greenflow Life에 오신 것을 환영합니다!
              </h2>
              <p className="text-gray-600 mb-6">
                음식을 통한 탄소 발자국 관리와 지속 가능한 식생활을 시작해보세요.
              </p>
              <div className="grid grid-cols-2 gap-4 text-sm text-gray-500">
                <div className="text-center">
                  <div className="text-2xl mb-2">📊</div>
                  <p>탄소 발자국 계산</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-2">🔄</div>
                  <p>스마트 대안 추천</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-2">🏆</div>
                  <p>챌린지 & 배지</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-2">📈</div>
                  <p>진행률 추적</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Router>
  );
}

export default App; 