from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# # class of model
# class Model:
#     def __init__(self, fun, param_names, var_names):
#         Model.fun = fun
#         Model.params = param_names
#         Model.vars = var_names

class Models:
    # note: order of x and t is swapped compared to earlier because we now use solve_ivp instead of odeint
    def SIRDS(self, t, x0, beta, gamma, delta, omega):
        # note diff eqs don't change with time, so t is not used
        S, I, R, D = x0
        Sprime = -beta * S * I + omega * R
        Iprime =  beta * S * I - gamma * I - delta * I
        Rprime = gamma * I - omega * R
        Dprime = delta * I
        return (Sprime, Iprime, Rprime, Dprime)
    

mods = Models()

# class of simulation
class Sim:
    def __init__(self, model_name, params, inits, t1, t0=0):
        self.model = model_name
        self.params = params
        self.inits = inits
        self.n_var = len(inits)
        self.t0 = t0
        self.t1 = t1
        self.solved = False
        self.backsums_calc = False
    
    def solve(self):
        sim = solve_ivp(getattr(mods, self.model), 
                        t_span=(self.t0, self.t1), 
                        y0=self.inits, args=self.params, 
                        method='RK45', rtol=1e-9, atol=1e-12)
        if sim.success:
            self.solved = True
            self.ts = sim.t
            self.data = sim.y
            self.finalD = self.data[-1][-1]
        else:
            return False
    
    def calc_backsums(self):
        if self.backsums_calc:
            return -1
        elif self.solved:            
            backsums = [self.data[-1]]
            for i in range(self.n_var-1):
                backsums.append(backsums[-1]+self.data[2-i])
            
            self.backsums = backsums
            self.backsums_calc = True
        else:
            return -2
    
    def plot_on_axis(self, ax):
        if self.solved:
            ax.fill_between(self.ts, self.backsums[2], self.backsums[3], color='black', label='S', alpha=0.1)
            ax.fill_between(self.ts, self.backsums[1], self.backsums[2], color='red',   label='I', alpha=0.4)
            ax.fill_between(self.ts, self.backsums[0], self.backsums[1], color='green', label='R', alpha=0.2)
            ax.fill_between(self.ts, 0,                self.backsums[0], color='black', label='D', alpha=0.5)

            for i in range(self.n_var-1):
                ax.plot(self.ts, self.backsums[i], color='black', linewidth=0.8)


# beta = 0.6      # infection rate
# gamma = 0.2    # recovery rate
# delta = 0.003   # death rate
# omega = 0.006  # loss of immunity rate
#           (0.6, 0.12, 0.004, 0.006), 


def SIRDS365(params):
    return Sim("SIRDS", params,
           (1-0.00000003, 0.00000003, 0, 0),
           365)




# for i in range(2):
#     for j in range(2):
#         print(sims[i][j].params)
#         print(i,j,sims[i][j].finalD)



def plot365(params):
    tempsim = Sim("SIRDS", params, (1-0.00000003, 0.00000003, 0, 0), 365)
    fig, ax = plt.subplots(1)
    tempsim.solve()
    tempsim.calc_backsums()
    tempsim.plot_on_axis(ax)
    # plt.legend(loc=(0.86,0.7)) # top right
    # plt.legend(loc=(0.06, 0.7)) # top left
    #plt.title("SIRDS model, " + r"$\beta$" + f" = {beta}, " + r"$\gamma$" + f" = {gamma}, " + r"$\delta$" + f" = {delta}, " + r"$\omega$" + f" = {omega}")
    plt.show()


def plotfour365(pps, save=-1):
    p1,p2,p3,p4 = pps
    sims = [[0,0],[0,0]]
    sims[0][0] = SIRDS365(p1)
    sims[0][1] = SIRDS365(p2)
    sims[1][0] = SIRDS365(p3)
    sims[1][1] = SIRDS365(p4)

    for i in range(2):
        for j in range(2):
            sims[i][j].solve()
            sims[i][j].calc_backsums()

    plt.figure(figsize=(12, 12))

    fig, axs = plt.subplots(2, 2)
    
    finD = [[0,0],[0,0]]


    for i in range(2):
        for j in range(2):
            sims[i][j].plot_on_axis(axs[i][j])
            finD[i][j] = sims[i][j].finalD

    
    if not save==-1:
        fname = save+".svg"
        plt.savefig(fname)

    plt.show()
        
    return finD

    
testparams = ((0.6, 0.12, 0.004, 0.006),
              (0.3, 0.12, 0.004, 0.006),
              (0.6, 0.12, 0.002, 0.006),
              (0.3, 0.12, 0.002, 0.006))

tps2 = ((0.6, 0.12, 0.004, 0.006),
        (0.3, 0.12, 0.004, 0.006),
        (0.6, 0.12, 0.002, 0.006),
        (0.45, 0.12, 0.003, 0.006))

def test_tps2():
    ds = plotfour365(tps2)
    for i in range(2):
        for j in range(2):
            print(i,j,ds[i][j])

