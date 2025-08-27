# utils/evaluator.py - COMPLETE FILE
import numpy as np
from statistics import mean, stdev

class ShotEvaluator:
    def __init__(self):
        pass
    
    def evaluate_shot(self, frame_metrics):
        """Evaluate the complete shot"""
        if not frame_metrics:
            return self.get_default_evaluation()
        
        # Calculate category scores
        footwork_score = self.evaluate_footwork(frame_metrics)
        head_position_score = self.evaluate_head_position(frame_metrics)
        swing_control_score = self.evaluate_swing_control(frame_metrics)
        balance_score = self.evaluate_balance(frame_metrics)
        follow_through_score = self.evaluate_follow_through(frame_metrics)
        
        # Overall analysis
        overall_score = mean([
            footwork_score['score'],
            head_position_score['score'],
            swing_control_score['score'],
            balance_score['score'],
            follow_through_score['score']
        ])
        
        evaluation = {
            'overall_score': round(overall_score, 1),
            'total_frames_analyzed': len(frame_metrics),
            'scores': {
                'footwork': footwork_score,
                'head_position': head_position_score,
                'swing_control': swing_control_score,
                'balance': balance_score,
                'follow_through': follow_through_score
            },
            'recommendations': self.get_recommendations(frame_metrics)
        }
        
        return evaluation
    
    def evaluate_footwork(self, frame_metrics):
        """Evaluate footwork"""
        foot_directions = [m['foot_direction'] for m in frame_metrics if m['foot_direction'] is not None]
        
        if not foot_directions:
            return {'score': 5, 'feedback': 'Could not analyze foot direction'}
        
        avg_foot_angle = mean(foot_directions)
        
        if 45 <= avg_foot_angle <= 60:
            score = 9
        elif 35 <= avg_foot_angle <= 70:
            score = 7
        else:
            score = 5
        
        return {
            'score': score,
            'feedback': f'Foot angle: {avg_foot_angle:.1f}°. ' + 
                       ('Good positioning' if score >= 7 else 'Improve foot placement')
        }
    
    def evaluate_head_position(self, frame_metrics):
        """Evaluate head position"""
        alignments = [m['head_knee_alignment'] for m in frame_metrics if m['head_knee_alignment'] is not None]
        
        if not alignments:
            return {'score': 5, 'feedback': 'Could not analyze head position'}
        
        avg_alignment = mean(alignments)
        
        if avg_alignment < 0.03:
            score = 9
        elif avg_alignment < 0.05:
            score = 7
        else:
            score = 5
        
        return {
            'score': score,
            'feedback': f'Head stability good' if score >= 7 else 'Keep head over front knee'
        }
    
    def evaluate_swing_control(self, frame_metrics):
        """Evaluate swing control"""
        elbow_angles = [m['elbow_angle'] for m in frame_metrics if m['elbow_angle'] is not None]
        
        if not elbow_angles:
            return {'score': 5, 'feedback': 'Could not analyze swing mechanics'}
        
        avg_elbow = mean(elbow_angles)
        
        if 110 <= avg_elbow <= 140:
            score = 9
        elif 100 <= avg_elbow <= 150:
            score = 7
        else:
            score = 5
        
        return {
            'score': score,
            'feedback': f'Elbow positioning ' + ('excellent' if score >= 8 else 'needs work')
        }
    
    def evaluate_balance(self, frame_metrics):
        """Evaluate balance"""
        balance_scores = [m['balance_score'] for m in frame_metrics if m['balance_score'] is not None]
        
        if not balance_scores:
            return {'score': 6, 'feedback': 'Balance analysis limited'}
        
        avg_balance = mean(balance_scores)
        score = min(10, max(1, avg_balance * 10))
        
        return {
            'score': round(score, 1),
            'feedback': 'Good balance' if score >= 7 else 'Work on stability'
        }
    
    def evaluate_follow_through(self, frame_metrics):
        """Evaluate follow-through"""
        if len(frame_metrics) < 10:
            return {'score': 6, 'feedback': 'Limited follow-through data'}
        
        last_third = frame_metrics[2*len(frame_metrics)//3:]
        spine_leans = [m['spine_lean'] for m in last_third if m['spine_lean'] is not None]
        
        if spine_leans:
            avg_lean = mean(spine_leans)
            if 15 <= avg_lean <= 25:
                score = 8
            else:
                score = 6
        else:
            score = 5
        
        return {
            'score': score,
            'feedback': 'Good completion' if score >= 7 else 'Focus on follow-through'
        }
    
    def get_recommendations(self, frame_metrics):
        """Generate recommendations"""
        recommendations = []
        
        elbow_angles = [m['elbow_angle'] for m in frame_metrics if m['elbow_angle'] is not None]
        if elbow_angles and mean(elbow_angles) < 110:
            recommendations.append("Work on getting the front elbow higher during the shot")
        
        alignments = [m['head_knee_alignment'] for m in frame_metrics if m['head_knee_alignment'] is not None]
        if alignments and mean(alignments) > 0.05:
            recommendations.append("Focus on keeping your head over the front knee")
        
        spine_leans = [m['spine_lean'] for m in frame_metrics if m['spine_lean'] is not None]
        if spine_leans and mean(spine_leans) > 25:
            recommendations.append("Try to maintain a more upright posture during the shot")
        
        if not recommendations:
            recommendations.append("Overall technique looks good! Continue practicing for consistency")
        
        return recommendations
    
    def get_default_evaluation(self):
        """Default evaluation when no data"""
        return {
            'overall_score': 0,
            'total_frames_analyzed': 0,
            'scores': {
                'footwork': {'score': 0, 'feedback': 'No data available'},
                'head_position': {'score': 0, 'feedback': 'No data available'},
                'swing_control': {'score': 0, 'feedback': 'No data available'},
                'balance': {'score': 0, 'feedback': 'No data available'},
                'follow_through': {'score': 0, 'feedback': 'No data available'}
            },
            'recommendations': ['Unable to analyze - ensure clear view of player']
        }
