from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import tkinter as tk
from tkinter import ttk,filedialog, messagebox
import pandas as pd 

# ------------------------------- Main application ------------------------------------------------------------------------------------

class Quantumportfolio:
    def __init__(self,root):
        self.root=root
        self.root.title("Quantum Portfolio Optimizer")
        self.root.geometry("1200x750")
        self.root.configure(bg="#0D0D0D")

        self.stocks=[]
        self.returns=[]
        self.risks=[]
        self.create_widgets()
    def create_widgets(self):
        leftframe=tk.Frame(self.root,bg="#1A1026")
        leftframe.pack(side=tk.LEFT,padx=10,pady=10,fill=tk.Y)
        rightframe=tk.Frame(self.root,bg="#12091C")
        rightframe.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=10,pady=10)
        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground="#2B2B2B",
            background="#7B2CBF",
            foreground="white",
            arrowcolor="white"
        )

        style.configure(
            "Treeview",
            background="#1B1B1B",
            foreground="white",
            fieldbackground="#1B1B1B",
            rowheight=30,
            font=("Segoe UI",10)
        )

        style.configure(
            "Treeview.Heading",
            background="#5A189A",
            foreground="white",
            font=("Segoe UI",11,"bold")
        )

        style.map(
            "Treeview",
            background=[("selected","#9D4EDD")]
        )
        tk.Label(
                leftframe,
                text="Stock Name",
                bg="#1A1026",
                fg="white",
                font=("Segoe UI",11,"bold")
                ).pack()
        self.stockentry=tk.Entry(leftframe)
        self.stockentry.pack()
        tk.Label(
                leftframe,
                text="Expected return of stock",
                bg="#1A1026",
                fg="white",
                font=("Segoe UI",11,"bold")
                ).pack()
        self.return_entry=tk.Entry(leftframe)
        self.return_entry.pack()
        tk.Label(
                leftframe,
                text="Expected Risk of stock",
                bg="#1A1026",
                fg="white",
                font=("Segoe UI",11,"bold")
                ).pack()
        self.risk_entry=tk.Entry(leftframe)
        self.risk_entry.pack()
        tk.Button(
            leftframe,
            text="Add stock here",command=self.add_stock,
            bg="#7B2CBF",
            fg="white",
            activebackground="#9D4EDD",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI",10,"bold"),
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(pady=5)
        tk.Label(
                leftframe,
                text="Investor profile",
                bg="#1A1026",
                fg="white",
                font=("Segoe UI",11,"bold")
                ).pack()
        self.profile=tk.StringVar()
        profilebox=ttk.Combobox(leftframe,textvariable=self.profile,
                                values=
                                ["Aggressive","Balanced","Conservative"])
        profilebox.current(1)
        profilebox.pack()
        tk.Button(
            leftframe,
            text="Run Optimization",
            command=self.run_optimization,
            bg="#7B2CBF",
            fg="white",
            activebackground="#9D4EDD",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI",10,"bold"),
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(pady=5)
        tk.Button(
            leftframe,
            text="Import CSV",command=self.importcsv,
            bg="#7B2CBF",
            fg="white",
            activebackground="#9D4EDD",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI",10,"bold"),
            padx=10,
            pady=5,
            cursor="hand2"
        ).pack(pady=5)
        tk.Button(leftframe,text="Export Results",command=self.Exportresult,bg="#7B2CBF",fg="white",
                  activebackground="#9D4EDD",activeforeground="white",
                  relief="flat",font=("Segeo UI",10,"bold"),padx=10,pady=5,cursor="hand2").pack(pady=5)
        self.tree=ttk.Treeview(rightframe,columns=("stocks","returns","risks"),show="headings")
        self.tree.heading("stocks",text="Stocks")
        self.tree.heading("returns",text="Returns")
        self.tree.heading("risks",text="Risks")
        self.tree.pack(fill=tk.BOTH,expand=True)
        self.result_text=tk.Text(
                        rightframe,
                        height=12,
                        bg="#1B1B1B",
                        fg="white",
                        insertbackground="white",
                        font=("Consolas",11),
                        relief="flat"
                    )
        self.result_text.pack(fill=tk.X,pady=10)

#--------------------------------- Adding the stocks -----------------------------------------------------------------

    def add_stock(self):
        try:
            name=self.stockentry.get()
            ret=float(self.return_entry.get())
            ris=float(self.risk_entry.get())
            self.stocks.append(name)
            self.returns.append(ret)
            self.risks.append(ris)
            self.tree.insert("",tk.END,values=(name,ret,ris))
            self.stockentry.delete(0,tk.END)
            self.return_entry.delete(0,tk.END)
            self.risk_entry.delete(0,tk.END)
        except ValueError:
            messagebox.showerror(
                "Error","Invalid input"
            )
     #----------------------------------- Profile ----------------------------------------------------------------------
        

    def get_weights(self):
        profile=self.profile.get()
        if profile=="Aggressive":
            return 0.8,0.2
        elif profile=="Balanced":
            return 0.5,0.5
        else:
            return 0.3,0.7
        
#------------------------- Quantum optimization --------------------------------------------------------------------------

    def run_optimization(self):
        if len(self.stocks)==0:
            messagebox.showwarning("Warning","Add stocks first")
            return
        return_weight,risk_weight=(self.get_weights())
        scores=[]
        for r,k in zip(self.returns,self.risks):
            score=(r*return_weight-k*risk_weight)
            scores.append(score)
        n=len(self.stocks)
        qc=QuantumCircuit(n,n)
        for i in range(n):
            qc.h(i)
        gamma=0.3
        for i in range(n):
            qc.rz(-2*gamma*scores[i],i)
        beta=0.5
        for i in range(n):
            qc.rx(2*beta,i)
        qc.measure(range(n),range(n))
        ssimulator=AerSimulator()
        job=ssimulator.run(qc,shots=1024)
        results=job.result()
        counts=results.get_counts()
        plot_histogram(counts)
        plt.title("Results")
        plt.show(block=False)
        beststate=max(counts,key=counts.get)
        selected=[]
        total_return=0
        total_risk=0
        for i in range(n):
            if beststate[n-1-i]=="1":
                selected.append(self.stocks[i])
                total_return+=self.returns[i]
                total_risk+=self.risks[i]
        score=(return_weight*total_return-risk_weight*total_risk)
        self.result_text.delete(
            "1.0",tk.END
        )
        self.result_text.insert(
            tk.END,
            f"Best Portfolio state:"
            f"{beststate}\n\n"
        )
        self.result_text.insert(
            tk.END,
            "Selected stocks\n"
        )
        for stock in selected:
            self.result_text.insert(
                tk.END,
                stock+"\n"
            )
        self.result_text.insert(
            tk.END,
            "Total returns:\n"
            f"{total_return:.2f}"
        )
        self.result_text.insert(
            tk.END,
            "Total risk:\n"
            f"{total_risk:.2f}"
        )
        self.result_text.insert(
            tk.END,
            "Total Portfolio score\n"
            f"{score:.2f}"
        )
        print(qc)
    def importcsv(self):
        file=filedialog.askopenfilename(
            filetypes=[("CSV Files","*.csv")]
        )
        if not file:
            return
        df=pd.read_csv(file)
        self.stocks.clear()
        self.returns.clear()
        self.risks.clear(
        )
        for item in self.tree.get_children():
            self.tree.delete(item)
        for _,row in df.iterrows():
            self.stocks.append(row["Stock"])
            self.returns.append(row["Return"])
            self.risks.append(row["Risk"])
            self.tree.insert(
                "",
                tk.END,
                values=(row["Stock"],row["Return"],row["Risk"])
            )

        
#----------------------------------------- Export results -------------------------------------------------------------------------------------------------------------------
    
    def Exportresult(self):
        content=self.result_text.get(
            "1.0",tk.END
        )
        FILE=filedialog.asksaveasfilename(
            defaultextension=".txt"
        )
        if FILE:
            with open(FILE,"w") as f:
                f.write(content)
            messagebox.showinfo(
                "Results Exported","Saved"
            )
        
            


            
#--------------------------------------------------------- Run application ---------------------------------------------------------------------------------------------------
root=tk.Tk()
app=Quantumportfolio(root)
root.mainloop()





    

