import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import csv
from tkinter import filedialog


class Courses:
    def __init__(self, root):
        self.classes_and_years = {}
        self.selected_classes = []

        FilePathLbl = Label(root, width=15)
        FilePathLbl.config(text="Provide data path", bg="white")
        FilePathLbl.grid(row=0, column=0, padx=(5, 10), pady=(20, 0))

        self.PathEntry = Entry(root)
        self.PathEntry.grid(
            row=0, column=1, padx=(0, 0), pady=(20, 0), columnspan=2, sticky=W + E
        )
        self.PathEntry.insert(END, "C:\\Users\\PC\\Downloads\\sampledata (1).csv")

        YrLbl = Label(root, width=15)
        YrLbl.config(text="Year", bg="white")
        YrLbl.grid(row=1, column=0, padx=(5, 10), pady=(20, 0), sticky=W + E)
        n = tk.StringVar()

        self.YrBox = ttk.Combobox(root, width=5, textvariable=n)
        self.YrBox["values"] = ("1", "2", "3", "4", "5")
        self.YrBox.grid(column=1, row=1, padx=(5, 10), pady=(20, 0), sticky=W + E)
        self.YrBox.current()

        DepLbl = Label(root)
        DepLbl.config(text="Department", bg="white")
        DepLbl.grid(row=1, column=3, padx=(5, 10), pady=(20, 0), sticky=W + E)

        self.DpEntry = Entry(root)
        self.DpEntry.grid(row=1, column=4, padx=(5, 10), pady=(20, 0), sticky=W)

        DspBtn = Button(
            root,
            command=lambda: [
                self.enter_file_dir(),
                self.enter_year(),
                self.enter_dep(),
            ],
        )
        DspBtn.config(text="Display", bg="white")
        DspBtn.grid(row=2, column=0, sticky=E, padx=(0, 10), pady=(50, 0))

        ClrBtn = Button(root, command=self.clear_file_dir)
        ClrBtn.config(text="Clear", bg="white")
        ClrBtn.grid(row=2, column=1, sticky=W + E, padx=(0, 10), pady=(50, 0))

        SvBtn = Button(root)
        SvBtn.config(text="Save", bg="white")
        SvBtn.grid(row=2, column=2, sticky=W + E, padx=(0, 10), pady=(50, 0))

        SelCrsLbl = Label(root)
        SelCrsLbl.config(text="Selected courses: ", bg="white")
        SelCrsLbl.grid(
            row=5, column=0, columnspan=5, padx=(10, 0), pady=(50, 0), ipadx=5, sticky=W
        )

        self.SelCrsLbx = Listbox(root, width=70)
        self.SelCrsLbx.grid(row=6, column=0, columnspan=5, padx=(10, 0), pady=(15, 0), sticky=W)

        CrsLbl = Label(root)
        CrsLbl.config(text="Courses", bg="white")
        CrsLbl.grid(
            row=5, column=2, columnspan=10, padx=(0, 0), pady=(50, 0), sticky=W + E
        )

        self.CrsLbx = Listbox(root, width=70)
        self.CrsLbx.grid(
            row=6, column=2, columnspan=10, padx=(0, 0), pady=(15, 0), sticky=W + E
        )

        def moveTo(fromList, toList):
            indexList = fromList.curselection()
            # print(indexList)
            if indexList:
                index = indexList[0]
                val = fromList.get(index)
                separated = val.split(" - ")
                print("Separated is", separated[0])
                if self.select_a_class(separated[0]):
                    fromList.delete(index)
                    toList.insert(END, val)

        move_to_lambda = lambda x: moveTo(self.CrsLbx, self.SelCrsLbx)
        self.CrsLbx.bind("<Double-1>", move_to_lambda)

    def parse(self, row):
        entry = row[0].split(" ")
        class_name = entry[0]  # shkurtesa e klasave
        class_year = int(entry[1][0][0])  # numri i par o vitet

        schedule = {}
        time = row[3].split(" ")

        days = row[2].split(" ")
        for day in days:
            if len(day) == 0:
                continue
            schedule[day] = []

        # Each index of time(range) corresponds to a day
        for idx, entry in enumerate(time):
            if len(entry) == 0:
                continue
            range_elements = entry.split("-")

            min_range = int(range_elements[0].split(":")[0])  # 10
            max_range = int(range_elements[1].split(":")[0])  # 13

            day = days[idx]
            if not day:
                print("Bad data")

            schedule[day] = [min_range, max_range]
            print(schedule)

        return {
            "year": class_year,
            "name": row[0],
            "fullname": row[1],
            "schedule": schedule,
            "time": row[3],
            "days": row[2]
        }


    def select_a_class(self, class_name):
        print("Class name is", class_name)
        class_object = self.classes_and_years[class_name]
        for selected in self.selected_classes:
            selected_class_object = self.classes_and_years[selected]
            for day in class_object["schedule"]:
                print(selected_class_object, day)
                min_for_selected = selected_class_object[day][0]
                max_for_selected = selected_class_object[day][1]

                min_for_current = class_object["schedule"][day][0]
                max_for_current = class_object["schedule"][day][1]

                if (min_for_current > min_for_selected and max_for_current < max_for_selected):
                    # overlap
                    print("Overlap, don't allow")
                    return False
        self.selected_classes.append(class_name)
        return True

    # C:\\Users\\PC\\Downloads\\sampledata (1).csv
    def enter_file_dir(self):
        self.CrsLbx.delete(0, END)
        with open("C:\\Users\\PC\\Downloads\\sampledata (1).csv", mode="r") as file:
            sd = csv.reader(file)
            for row in sd:
                self.classes_and_years[row[0]] = self.parse(row)
                print("Parsed row is", row[0])
                print(self.classes_and_years[row[0]])

        filepath = self.PathEntry.get()
        year = self.YrBox.get()
        department = self.DpEntry.get()

        if year == "" or department == "":
            print("kah je nis")
        else:
            found = []
            for obj in self.classes_and_years.values():
                if int(year) == obj["year"] and obj["name"].startswith(department):
                    found.append(obj)
                    self.CrsLbx.insert(
                        END,
                        obj["name"]
                        + " - "
                        + obj["fullname"]
                        + " - "
                        + obj["days"]
                        + " - "
                        + obj["time"],
                    )
            print(found)

    def clear_file_dir(self):
        self.SelCrsLbx.delete(0, END)
        self.selected_classes = []

    def enter_year(self):
        year = self.YrBox.get()
        print(year)

    def enter_dep(self):
        department = self.DpEntry.get()
        print(department)


root = Tk()
root.resizable(0, 0)  # disable window size
root.geometry("700x500+400+200")  # size of the window
root.wm_title(" " * 50 + "Course Tool")  # to set a title of the window
root.configure(background="dimgray")  # backgournd color
Courses(root)
root.mainloop()
