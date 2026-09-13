from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich.align import Align
from rich.text import Text
from rich import box
from time import sleep
from datetime import date

from services.auth_service import AuthService
from services.product_service import ProductService
from services.promotion_service import PromotionService
from services.sale_service import SaleService
from utils.decorators import require_role, audit

console=Console()

class PromoApp:
    def __init__(self):
        self.auth=AuthService(); self.products=ProductService(); self.promotions=PromotionService(); self.sales=SaleService(); self.current_user=None

    def splash(self):
        console.clear()
        with Progress(SpinnerColumn(), TextColumn("[bold cyan]Launching PromoFlow..."), transient=True) as progress:
            task=progress.add_task("", total=1)
            sleep(.25); progress.update(task, advance=1)
        title=Text("PROMOFLOW", style="bold white on blue")
        console.print(Panel(Align.center(title), subtitle="Discount & Promotion Management System", border_style="cyan", padding=(1,5)))
        console.print(Align.center("✨ Turn ordinary sales into smarter promotions. ✨\n"))
        sleep(.4)

    def header(self, title, subtitle=""):
        console.clear()
        console.print(Panel(f"[bold white]{title}[/bold white]\n[dim]{subtitle}[/dim]", border_style="cyan", box=box.DOUBLE))

    def menu(self, options):
        table=Table(box=box.ROUNDED, show_header=False, padding=(0,2))
        table.add_column("#", style="bold cyan", width=4); table.add_column("Action", style="white")
        for i,(label,icon) in enumerate(options,1): table.add_row(str(i),f"{icon} {label}")
        console.print(table)
        return Prompt.ask("[bold yellow]➜ Choose an option[/bold yellow]", choices=[str(i) for i in range(1,len(options)+1)])

    def run(self):
        self.splash()
        while True:
            self.header("🏪 PROMOFLOW", "Smart promotions • faster sales • better reports")
            choice=self.menu([("Login","🔐"),("Register Staff","👤"),("Exit","🚪")])
            if choice=="1": self.login()
            elif choice=="2": self.register_staff()
            else: console.print("[bold cyan]Goodbye! 👋[/bold cyan]"); break

    def login(self):
        self.header("🔐 Secure Login", "Enter your PromoFlow credentials")
        username=Prompt.ask("Username"); password=Prompt.ask("Password", password=True)
        user=self.auth.login(username,password)
        if not user:
            console.print("[bold red]✗ Login failed.[/bold red] Check your username/password."); Prompt.ask("Press Enter", default=""); return
        self.current_user=user
        console.print(Panel(f"[bold green]✓ Welcome back, {user.username}![/bold green]\nRole: {user.role.upper()}", border_style="green"))
        sleep(.7)
        self.admin_menu() if user.role=="admin" else self.staff_menu()

    def register_staff(self):
        self.header("👤 Staff Registration", "Create a staff account")
        try:
            u=Prompt.ask("Username"); p=Prompt.ask("Password", password=True); self.auth.register(u,p,"staff")
            console.print("[bold green]✓ Staff account created.[/bold green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter", default="")

    @require_role("admin")
    def admin_menu(self):
        while self.current_user:
            self.header(f"👑 ADMIN COMMAND CENTER — {self.current_user.username}", "Full system control")
            choice=self.menu([("Dashboard","📊"),("Product Management","📦"),("Promotion Management","🎯"),("Sales & Reports","💰"),("Manage Staff","👥"),("Logout","🚪")])
            if choice=="1": self.dashboard()
            elif choice=="2": self.product_menu()
            elif choice=="3": self.promotion_menu()
            elif choice=="4": self.sales_report()
            elif choice=="5": self.staff_list()
            else: self.current_user=None

    def dashboard(self):
        self.header("📊 Live Dashboard", "Your business at a glance")
        active=sum(1 for p in self.promotions.promotions if p.active and p.start_date<=date.today().isoformat()<=p.end_date)
        low=sum(1 for p in self.products.products if p.stock<10)
        table=Table(box=box.SIMPLE_HEAVY); table.add_column("Metric"); table.add_column("Value",justify="right")
        table.add_row("📦 Products",str(len(self.products.products))); table.add_row("🎯 Active Promotions",str(active)); table.add_row("🧾 Sales",str(len(self.sales.sales))); table.add_row("💵 Revenue",f"KSh {self.sales.total_revenue():,.2f}"); table.add_row("🏷️ Discounts Given",f"KSh {self.sales.total_discounts():,.2f}"); table.add_row("⚠️ Low Stock",str(low))
        console.print(table); Prompt.ask("Press Enter",default="")

    @require_role("admin")
    @audit("Product operation")
    def product_menu(self):
        while True:
            self.header("📦 Product Hub", "Manage your catalogue")
            c=self.menu([("List Products","📋"),("Add Product","➕"),("Edit Product","✏️"),("Delete Product","🗑️"),("Back","↩️")])
            if c=="1": self.list_products()
            elif c=="2": self.add_product()
            elif c=="3": self.edit_product()
            elif c=="4": self.delete_product()
            else: break

    def list_products(self):
        table=Table(title="📦 Product Catalogue",box=box.ROUNDED); [table.add_column(x) for x in ["ID","Product","Category","Price","Stock"]]
        for p in self.products.products: table.add_row(str(p.id),p.name,p.category,f"KSh {p.price:,.2f}",str(p.stock))
        console.print(table); Prompt.ask("Press Enter",default="")

    def add_product(self):
        try:
            p=self.products.add(Prompt.ask("Name"),Prompt.ask("Category"),FloatPrompt.ask("Price (KSh)"),IntPrompt.ask("Stock")); console.print(f"[green]✓ Added {p.name}[/green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def edit_product(self):
        self.list_products();
        try:
            pid=IntPrompt.ask("Product ID"); p=self.products.get(pid)
            if not p: raise ValueError("Product not found.")
            self.products.update(pid,Prompt.ask("Name",default=p.name),Prompt.ask("Category",default=p.category),FloatPrompt.ask("Price",default=p.price),IntPrompt.ask("Stock",default=p.stock)); console.print("[green]✓ Product updated.[/green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def delete_product(self):
        self.list_products();
        try:
            pid=IntPrompt.ask("Product ID")
            if Confirm.ask("Delete this product?"): self.products.delete(pid); console.print("[green]✓ Deleted.[/green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def promotion_menu(self):
        while True:
            self.header("🎯 Promotion Studio", "Design, activate and control offers")
            c=self.menu([("View Promotions","📋"),("Create Promotion","✨"),("Toggle Promotion","🔄"),("Delete Promotion","🗑️"),("Back","↩️")])
            if c=="1": self.list_promotions()
            elif c=="2": self.create_promotion()
            elif c=="3": self.toggle_promotion()
            elif c=="4": self.delete_promotion()
            else: break

    def list_promotions(self):
        table=Table(title="🎯 Promotion Board",box=box.ROUNDED); [table.add_column(x) for x in ["ID","Offer","Product","Discount","Dates","Status"]]
        for p in self.promotions.promotions:
            prod=self.products.get(p.product_id); status="🟢 ACTIVE" if p.active else "🔴 OFF"
            table.add_row(str(p.id),p.name,prod.name if prod else "Unknown",f"{p.discount_value:g}{'%' if p.discount_type=='percentage' else ' KSh'}",f"{p.start_date} → {p.end_date}",status)
        console.print(table); Prompt.ask("Press Enter",default="")

    def create_promotion(self):
        if not self.products.products: console.print("[yellow]Add a product first.[/yellow]"); Prompt.ask("Press Enter",default=""); return
        self.list_products()
        try:
            pid=IntPrompt.ask("Product ID");
            if not self.products.get(pid): raise ValueError("Product not found.")
            name=Prompt.ask("Promotion name"); dtype=Prompt.ask("Discount type",choices=["percentage","fixed"]); value=FloatPrompt.ask("Discount value"); start=Prompt.ask("Start date (YYYY-MM-DD)"); end=Prompt.ask("End date (YYYY-MM-DD)")
            self.promotions.add(name,pid,dtype,value,start,end); console.print("[bold green]✨ Promotion launched![/bold green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def toggle_promotion(self):
        self.list_promotions();
        try: self.promotions.toggle(IntPrompt.ask("Promotion ID")); console.print("[green]✓ Status changed.[/green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def delete_promotion(self):
        self.list_promotions();
        try:
            pid=IntPrompt.ask("Promotion ID")
            if Confirm.ask("Delete promotion?"): self.promotions.delete(pid); console.print("[green]✓ Deleted.[/green]")
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def staff_menu(self):
        while self.current_user:
            self.header(f"🛍️ SALES FLOOR — {self.current_user.username}", "Fast checkout • live promotions")
            c=self.menu([("Browse Products","📦"),("Live Promotions","🔥"),("Make a Sale","🧾"),("My Sales","📈"),("Logout","🚪")])
            if c=="1": self.list_products()
            elif c=="2": self.list_promotions()
            elif c=="3": self.make_sale()
            elif c=="4": self.my_sales()
            else: self.current_user=None

    def make_sale(self):
        self.header("🧾 Express Checkout", "Apply a live promotion and close the sale")
        try:
            if not self.products.products: raise ValueError("No products available.")
            self.list_products(); pid=IntPrompt.ask("Product ID"); product=self.products.get(pid)
            if not product: raise ValueError("Product not found.")
            qty=IntPrompt.ask("Quantity")
            if qty<=0 or qty>product.stock: raise ValueError(f"Quantity must be 1–{product.stock}.")
            customer=Prompt.ask("Customer name",default="Walk-in")
            promos=self.promotions.active_for_product(pid)
            promo=None
            if promos:
                console.print("[bold green]🔥 LIVE OFFERS[/bold green]")
                for p in promos: console.print(f"  [cyan]{p.id}[/cyan] — {p.name} — {p.discount_value:g}{'%' if p.discount_type=='percentage' else ' KSh'} off")
                selected=IntPrompt.ask("Promotion ID (0 for none)",default=0)
                if selected: promo=next((p for p in promos if p.id==selected),None)
            sale=self.sales.create(self.current_user.username,customer,product,qty,promo)
            console.print(Panel(f"[bold green]✓ SALE COMPLETE[/bold green]\n\nCustomer: {customer}\nProduct: {product.name}\nQuantity: {qty}\nOriginal: KSh {sale.original_total:,.2f}\nDiscount: [yellow]KSh {sale.discount_total:,.2f}[/yellow]\nFinal: [bold green]KSh {sale.final_total:,.2f}[/bold green]",border_style="green"))
        except ValueError as e: console.print(f"[red]✗ {e}[/red]")
        Prompt.ask("Press Enter",default="")

    def my_sales(self):
        rows=[s for s in self.sales.sales if s.staff_username==self.current_user.username]
        self.render_sales(rows,"📈 My Sales")

    def sales_report(self):
        self.render_sales(self.sales.sales,"💰 Sales Command Report")
        console.print(f"[bold cyan]Revenue:[/bold cyan] KSh {self.sales.total_revenue():,.2f}   [bold yellow]Discounts:[/bold yellow] KSh {self.sales.total_discounts():,.2f}")
        Prompt.ask("Press Enter",default="")

    def render_sales(self, rows,title):
        table=Table(title=title,box=box.ROUNDED); [table.add_column(x) for x in ["ID","Staff","Customer","Qty","Original","Discount","Final","Date"]]
        for s in rows: table.add_row(str(s.id),s.staff_username,s.customer_name,str(s.quantity),f"{s.original_total:,.2f}",f"{s.discount_total:,.2f}",f"{s.final_total:,.2f}",s.created_at[:10])
        console.print(table)

    def staff_list(self):
        self.header("👥 Staff Directory")
        table=Table(box=box.ROUNDED); table.add_column("Username"); table.add_column("Role")
        for u in self.auth.users: table.add_row(u.username,u.role.upper())
        console.print(table); Prompt.ask("Press Enter",default="")

if __name__=="__main__": PromoApp().run()
