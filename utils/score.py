import numpy as np

def rank_score(judge: dict, fan: dict):
    keys = list(judge.keys())

    judge_vals = np.array([judge[k] for k in keys])
    fan_vals = np.array([fan[k] for k in keys])
    
    judge_ranks = np.argsort(np.argsort(-judge_vals)) + 1
    fan_ranks = np.argsort(np.argsort(-fan_vals)) + 1
    
    combined_ranks = judge_ranks + fan_ranks
    
    return list(zip(keys, combined_ranks))

def percentage_score(judge: dict, fan: dict):
    keys = list(judge.keys())
    judge_vals = np.array([judge[k] for k in keys])
    fan_vals = np.array([fan[k] for k in keys])
    
    judge_pct = judge_vals / np.sum(judge_vals)
    fan_pct = fan_vals / np.sum(fan_vals)
    
    total_pct = judge_pct + fan_pct
    
    sorted_indices = np.argsort(-total_pct)
    
    result = [(keys[i], total_pct[i]) for i in sorted_indices]
    return result

if __name__ == '__main__':
    judge = {'player1': 9.6, 'player2': 9.4, 'player3': 9.2}
    fan = {'player1': 2312302, 'player2': 3312301, 'player3': 2312300}
    print(rank_score(judge, fan))
    print(percentage_score(judge, fan))
