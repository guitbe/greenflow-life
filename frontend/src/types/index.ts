// User types
export interface User {
  id: number;
  email: string;
  name: string;
  dietary_preference: 'omnivore' | 'vegetarian' | 'vegan' | 'pescatarian';
  target_carbon_reduction: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
  dietary_preference: 'omnivore' | 'vegetarian' | 'vegan' | 'pescatarian';
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Meal types
export type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';

export interface MealLog {
  id: number;
  food_name: string;
  portion_size: number;
  meal_type: MealType;
  carbon_footprint: number;
  image_url?: string;
  logged_at: string;
}

export interface MealCreate {
  food_name: string;
  portion_size: number;
  meal_type: MealType;
  image_url?: string;
}

// Carbon footprint types
export interface CarbonCalculationRequest {
  food_name: string;
  portion_size: number;
}

export interface CarbonCalculationResponse {
  food_name: string;
  portion_size: number;
  carbon_footprint: number;
  category: string;
  sustainability_rating: 'LOW' | 'MEDIUM' | 'HIGH';
}

// Dashboard types
export interface DashboardStats {
  total_carbon_this_week: number;
  carbon_reduction_achieved: number;
  target_progress_percentage: number;
  meals_logged_this_week: number;
  swaps_accepted: number;
  active_challenges: number;
  completed_challenges: number;
}

export interface CarbonTrend {
  date: string;
  carbon_amount: number;
  meal_count: number;
}

export interface TopContributor {
  food_name: string;
  total_carbon: number;
  frequency: number;
}

export interface InsightCard {
  type: 'achievement' | 'tip' | 'warning' | 'celebration';
  title: string;
  message: string;
  icon: string;
  action_text: string;
}

export interface DashboardData {
  stats: DashboardStats;
  carbon_trends: CarbonTrend[];
  top_contributors: TopContributor[];
  insights: InsightCard[];
}

// Swap types
export interface SwapRecommendation {
  original_food: string;
  recommended_food: string;
  carbon_reduction: number;
  carbon_reduction_percentage: number;
  recommendation_message: string;
  category: string;
}

export interface SwapResponse {
  meal_log_id: number;
  recommendations: SwapRecommendation[];
}

// Challenge types
export type ChallengeType = 'carbon_reduction' | 'meal_logging' | 'swap_acceptance' | 'weekly_goal';

export interface Challenge {
  id: number;
  name: string;
  description: string;
  challenge_type: ChallengeType;
  target_value: number;
  badge_icon?: string;
  duration_days: number;
  is_active: boolean;
}

export interface UserChallenge {
  id: number;
  challenge: Challenge;
  current_progress: number;
  completed: boolean;
  progress_percentage: number;
  started_at: string;
  completed_at?: string;
  days_remaining: number;
}

//  Badge types
export type BadgeType = 'daily_streak' | 'weekly_carbon' | 'monthly_carbon' | 'first_log' | 'eco_warrior' | 'swap_master' | 'challenge_champion';

export interface Badge {
  id: number;
  name: string;
  description: string;
  badge_type: BadgeType;
  requirement_value: number;
  icon_emoji: string;
  category?: string;
  criteria?: string;
}

export interface UserBadge {
  id: number;
  badge: Badge;
  earned_at: string;
  progress_value: number;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface ApiError {
  detail: string;
  status: number;
} 