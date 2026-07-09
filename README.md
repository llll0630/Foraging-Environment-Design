For how to use the playback API:<br>
get_grid() -- 把墙体信息暴露出来<br>
load_state(state, grid) -- 把存下来的信息返回环境内部<br>
# ---- 录制时（负责pipeline的同学的代码里）----<br>
env = ForagingEnv()<br>
state = env.reset(difficulty=2)<br>
grid = env.get_grid()          # 存一次，整局都用这个grid<br>
# 把 grid 写进 meta.json<br>

# ---- replay时 ----<br>
env = ForagingEnv()<br>
for step_record in log:<br>
    env.load_state(step_record["env_state"], grid)   # 还原到那一步<br>
    env.render(f"replay_step_{step_record['t']}.png") # 画出那帧<br>



There are some photos<br>
start:<br>
<img width="600" height="600" alt="final_1_start" src="https://github.com/user-attachments/assets/bc4c42d6-ba65-4119-bf6e-d12cc31a5d1c" /><br>

at resource<br>
<img width="600" height="600" alt="final_2_at_resource" src="https://github.com/user-attachments/assets/d67f5842-60b9-45cd-a718-b37ec539dcd5" /><br>

carrying<br>
<img width="600" height="600" alt="final_3_carrying" src="https://github.com/user-attachments/assets/2b5bbe7e-0a9e-4d9b-989b-bffdaa6c83fd" /><br>

facing down<br>
<img width="600" height="600" alt="final_4_facing_down" src="https://github.com/user-attachments/assets/10d8307b-2161-4303-8a04-f662c6a4681a" /><br>




Besides, examples for different difficulty levels are presented:<br>

Difficulty 3<br>
<img width="600" height="600" alt="difficulty_3" src="https://github.com/user-attachments/assets/cd3e8a9e-67c6-48f2-9b7a-fbb5170fc3dd" /><br>

Difficulty 2<br>
<img width="600" height="600" alt="difficulty_2" src="https://github.com/user-attachments/assets/e7d10f5d-800e-4ba5-b9b1-91938dd43f6f" /><br>

Difficulty 1<br>
<img width="600" height="600" alt="difficulty_1" src="https://github.com/user-attachments/assets/5d88b829-21f7-4d68-a9ce-2fbfd3c5b160" /><br>
