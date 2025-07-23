import axios, { AxiosInstance } from 'axios';
import {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  User,
  MealLog,
  MealCreate,
  CarbonCalculationRequest,
  CarbonCalculationResponse,
  DashboardData,
  SwapResponse,
  Challenge,
  UserChallenge
} from '../types';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    // Determine API URL based on environment with comprehensive detection
    const getApiUrl = () => {
      // Check if we're on any Vercel deployment
      const hostname = window.location.hostname;
      const isVercelDeploy = hostname.includes('vercel.app') || hostname.includes('vercel.com');
      
      // Production: use Render backend for any Vercel deployment
      if (isVercelDeploy) {
        console.log('🚀 Detected Vercel deployment, using production API');
        return 'https://greenflow-life.onrender.com/api';
      }
      
      // Development: use environment variable or localhost
      const devUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
      console.log('🔧 Using development API:', devUrl);
      return devUrl;
    };

    this.api = axios.create({
      baseURL: getApiUrl(),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          console.log('🔑 Authentication failed - redirecting to login');
          localStorage.removeItem('access_token');
          // Only redirect if not already on login page
          if (!window.location.pathname.includes('onboarding')) {
            window.location.href = '/onboarding';
          }
        } else if (error.response?.status === 403) {
          console.log('🚫 Access forbidden - token may be invalid');
          localStorage.removeItem('access_token');
          // Only redirect if not already on login page
          if (!window.location.pathname.includes('onboarding')) {
            window.location.href = '/onboarding';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/login', credentials);
    localStorage.setItem('access_token', response.data.access_token);
    return response.data;
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/register', userData);
    localStorage.setItem('access_token', response.data.access_token);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/auth/me');
    return response.data;
  }

  logout(): void {
    localStorage.removeItem('access_token');
  }

  // Meals
  async createMealLog(mealData: MealCreate): Promise<MealLog> {
    const response = await this.api.post<MealLog>('/meals/', mealData);
    return response.data;
  }

  async getMealLogs(skip: number = 0, limit: number = 50): Promise<MealLog[]> {
    const response = await this.api.get<MealLog[]>(`/meals/?skip=${skip}&limit=${limit}`);
    return response.data;
  }

  async getMealLog(mealId: number): Promise<MealLog> {
    const response = await this.api.get<MealLog>(`/meals/${mealId}`);
    return response.data;
  }

  // Carbon footprint
  async calculateCarbonFootprint(data: CarbonCalculationRequest): Promise<CarbonCalculationResponse> {
    const response = await this.api.post<CarbonCalculationResponse>('/footprint/calculate', data);
    return response.data;
  }

  async getDailyCarbonSummary(days: number = 7): Promise<any[]> {
    const response = await this.api.get(`/footprint/daily-summary?days=${days}`);
    return response.data;
  }

  // Dashboard
  async getDashboardData(): Promise<DashboardData> {
    const response = await this.api.get<DashboardData>('/dashboard/');
    return response.data;
  }

  // Swaps
  async getSwapRecommendations(mealId: number): Promise<SwapResponse> {
    const response = await this.api.get<SwapResponse>(`/swaps/${mealId}`);
    return response.data;
  }

  async acceptSwapRecommendation(swapId: number, accepted: boolean): Promise<any> {
    const response = await this.api.post('/swaps/accept', { swap_id: swapId, accepted });
    return response.data;
  }

  // Challenges
  async getAvailableChallenges(): Promise<Challenge[]> {
    const response = await this.api.get<Challenge[]>('/challenges/available');
    return response.data;
  }

  async getMyChallenges(): Promise<UserChallenge[]> {
    const response = await this.api.get<UserChallenge[]>('/challenges/my-challenges');
    return response.data;
  }

  async joinChallenge(challengeId: number): Promise<any> {
    const response = await this.api.post('/challenges/join', { challenge_id: challengeId });
    return response.data;
  }

  async updateChallengeProgress(challengeId: number, progressValue: number): Promise<any> {
    const response = await this.api.patch('/challenges/update-progress', {
      challenge_id: challengeId,
      progress_value: progressValue
    });
    return response.data;
  }

  // Generic GET method
  async get<T = any>(url: string): Promise<T> {
    const response = await this.api.get<T>(url);
    return response.data;
  }

  // Generic POST method
  async post<T = any>(url: string, data?: any): Promise<T> {
    const response = await this.api.post<T>(url, data);
    return response.data;
  }

  // Badges
  async getBadges(): Promise<any[]> {
    const response = await this.api.get('/gamification/badges');
    return response.data;
  }

  async getUserBadges(): Promise<any[]> {
    const response = await this.api.get('/gamification/my-badges');
    return response.data;
  }
}

export const apiService = new ApiService(); 