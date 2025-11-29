using System;
using System.CodeDom.Compiler;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Markup;
using Npgsql;

namespace InsecureVault;

public class DbManager : Window, IComponentConnector
{
	internal TabControl MainTabControl;

	internal DataGrid CompaniesDataGrid;

	internal DataGrid EmployeesDataGrid;

	internal DataGrid ProjectsDataGrid;

	internal DataGrid DocumentsDataGrid;

	internal TextBlock StatusTextBlock;

	private bool _contentLoaded;

	private string ConnectionString => BuildConnectionString();

	public DbManager()
	{
		//IL_0014: Unknown result type (might be due to invalid IL or missing references)
		//IL_001e: Expected O, but got Unknown
		InitializeComponent();
		((FrameworkElement)this).Loaded += new RoutedEventHandler(DbManager_Loaded);
	}

	private string BuildConnectionString()
	{
		return new NpgsqlConnectionStringBuilder
		{
			Host = "insecurevault.challs.m0lecon.it",
			Port = 5432,
			Database = "challenge",
			Username = "giovanni",
			Password = "801ffe68158341e34e07a42644b9c450"
		}.ConnectionString;
	}

	private void DbManager_Loaded(object sender, RoutedEventArgs e)
	{
		//IL_0043: Unknown result type (might be due to invalid IL or missing references)
		try
		{
			LoadCompanies();
			LoadEmployees();
			LoadProjects();
			LoadDocuments();
			StatusTextBlock.Text = "Connesso al database";
		}
		catch (Exception ex)
		{
			MessageBox.Show("Errore durante il caricamento dei dati: " + ex.Message, "Errore", (MessageBoxButton)0, (MessageBoxImage)16);
			StatusTextBlock.Text = "Errore di connessione";
		}
	}

	private void LoadCompanies()
	{
		using NpgsqlConnection npgsqlConnection = new NpgsqlConnection(ConnectionString);
		npgsqlConnection.Open();
		using NpgsqlCommand npgsqlCommand = new NpgsqlCommand("SELECT id, name, city, address, email, phone, vat_number FROM companies ORDER BY id", npgsqlConnection);
		using NpgsqlDataReader npgsqlDataReader = npgsqlCommand.ExecuteReader();
		ObservableCollection<Company> observableCollection = new ObservableCollection<Company>();
		while (npgsqlDataReader.Read())
		{
			observableCollection.Add(new Company
			{
				Id = npgsqlDataReader.GetInt32(0),
				Name = (npgsqlDataReader.IsDBNull(1) ? "" : npgsqlDataReader.GetString(1)),
				City = (npgsqlDataReader.IsDBNull(2) ? "" : npgsqlDataReader.GetString(2)),
				Address = (npgsqlDataReader.IsDBNull(3) ? "" : npgsqlDataReader.GetString(3)),
				Email = (npgsqlDataReader.IsDBNull(4) ? "" : npgsqlDataReader.GetString(4)),
				Phone = (npgsqlDataReader.IsDBNull(5) ? "" : npgsqlDataReader.GetString(5)),
				VatNumber = (npgsqlDataReader.IsDBNull(6) ? "" : npgsqlDataReader.GetString(6))
			});
		}
		((ItemsControl)CompaniesDataGrid).ItemsSource = observableCollection;
	}

	private void LoadEmployees()
	{
		using NpgsqlConnection npgsqlConnection = new NpgsqlConnection(ConnectionString);
		npgsqlConnection.Open();
		using NpgsqlCommand npgsqlCommand = new NpgsqlCommand("SELECT id, first_name, last_name, email, phone, department, position, salary, hire_date FROM employees ORDER BY id", npgsqlConnection);
		using NpgsqlDataReader npgsqlDataReader = npgsqlCommand.ExecuteReader();
		ObservableCollection<Employee> observableCollection = new ObservableCollection<Employee>();
		while (npgsqlDataReader.Read())
		{
			observableCollection.Add(new Employee
			{
				Id = npgsqlDataReader.GetInt32(0),
				FirstName = (npgsqlDataReader.IsDBNull(1) ? "" : npgsqlDataReader.GetString(1)),
				LastName = (npgsqlDataReader.IsDBNull(2) ? "" : npgsqlDataReader.GetString(2)),
				Email = (npgsqlDataReader.IsDBNull(3) ? "" : npgsqlDataReader.GetString(3)),
				Phone = (npgsqlDataReader.IsDBNull(4) ? "" : npgsqlDataReader.GetString(4)),
				Department = (npgsqlDataReader.IsDBNull(5) ? "" : npgsqlDataReader.GetString(5)),
				Position = (npgsqlDataReader.IsDBNull(6) ? "" : npgsqlDataReader.GetString(6)),
				Salary = (npgsqlDataReader.IsDBNull(7) ? 0m : npgsqlDataReader.GetDecimal(7)),
				HireDate = (npgsqlDataReader.IsDBNull(8) ? DateTime.MinValue : npgsqlDataReader.GetDateTime(8))
			});
		}
		((ItemsControl)EmployeesDataGrid).ItemsSource = observableCollection;
	}

	private void LoadProjects()
	{
		using NpgsqlConnection npgsqlConnection = new NpgsqlConnection(ConnectionString);
		npgsqlConnection.Open();
		using NpgsqlCommand npgsqlCommand = new NpgsqlCommand("SELECT id, name, description, status, budget, start_date, end_date FROM projects ORDER BY id", npgsqlConnection);
		using NpgsqlDataReader npgsqlDataReader = npgsqlCommand.ExecuteReader();
		ObservableCollection<Project> observableCollection = new ObservableCollection<Project>();
		while (npgsqlDataReader.Read())
		{
			observableCollection.Add(new Project
			{
				Id = npgsqlDataReader.GetInt32(0),
				Name = (npgsqlDataReader.IsDBNull(1) ? "" : npgsqlDataReader.GetString(1)),
				Description = (npgsqlDataReader.IsDBNull(2) ? "" : npgsqlDataReader.GetString(2)),
				Status = (npgsqlDataReader.IsDBNull(3) ? "" : npgsqlDataReader.GetString(3)),
				Budget = (npgsqlDataReader.IsDBNull(4) ? 0m : npgsqlDataReader.GetDecimal(4)),
				StartDate = (npgsqlDataReader.IsDBNull(5) ? ((DateTime?)null) : new DateTime?(npgsqlDataReader.GetDateTime(5))),
				EndDate = (npgsqlDataReader.IsDBNull(6) ? ((DateTime?)null) : new DateTime?(npgsqlDataReader.GetDateTime(6)))
			});
		}
		((ItemsControl)ProjectsDataGrid).ItemsSource = observableCollection;
	}

	private void LoadDocuments()
	{
		using NpgsqlConnection npgsqlConnection = new NpgsqlConnection(ConnectionString);
		npgsqlConnection.Open();
		using NpgsqlCommand npgsqlCommand = new NpgsqlCommand("SELECT id, title, document_type, file_path, is_confidential, created_at FROM documents ORDER BY id", npgsqlConnection);
		using NpgsqlDataReader npgsqlDataReader = npgsqlCommand.ExecuteReader();
		ObservableCollection<Document> observableCollection = new ObservableCollection<Document>();
		while (npgsqlDataReader.Read())
		{
			observableCollection.Add(new Document
			{
				Id = npgsqlDataReader.GetInt32(0),
				Title = (npgsqlDataReader.IsDBNull(1) ? "" : npgsqlDataReader.GetString(1)),
				DocumentType = (npgsqlDataReader.IsDBNull(2) ? "" : npgsqlDataReader.GetString(2)),
				FilePath = (npgsqlDataReader.IsDBNull(3) ? "" : npgsqlDataReader.GetString(3)),
				IsConfidential = (!npgsqlDataReader.IsDBNull(4) && npgsqlDataReader.GetBoolean(4)),
				CreatedAt = (npgsqlDataReader.IsDBNull(5) ? DateTime.MinValue : npgsqlDataReader.GetDateTime(5)),
				Content = "REDACTED"
			});
		}
		((ItemsControl)DocumentsDataGrid).ItemsSource = observableCollection;
	}

	[DebuggerNonUserCode]
	[GeneratedCode("PresentationBuildTasks", "10.0.0.0")]
	public void InitializeComponent()
	{
		if (!_contentLoaded)
		{
			_contentLoaded = true;
			Uri uri = new Uri("/InsecureVault;component/dbmanager.xaml", UriKind.Relative);
			Application.LoadComponent((object)this, uri);
		}
	}

	[DebuggerNonUserCode]
	[GeneratedCode("PresentationBuildTasks", "10.0.0.0")]
	[EditorBrowsable(EditorBrowsableState.Never)]
	void IComponentConnector.Connect(int connectionId, object target)
	{
		//IL_0024: Unknown result type (might be due to invalid IL or missing references)
		//IL_002e: Expected O, but got Unknown
		//IL_0031: Unknown result type (might be due to invalid IL or missing references)
		//IL_003b: Expected O, but got Unknown
		//IL_003e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0048: Expected O, but got Unknown
		//IL_004b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0055: Expected O, but got Unknown
		//IL_0058: Unknown result type (might be due to invalid IL or missing references)
		//IL_0062: Expected O, but got Unknown
		//IL_0065: Unknown result type (might be due to invalid IL or missing references)
		//IL_006f: Expected O, but got Unknown
		switch (connectionId)
		{
		case 1:
			MainTabControl = (TabControl)target;
			break;
		case 2:
			CompaniesDataGrid = (DataGrid)target;
			break;
		case 3:
			EmployeesDataGrid = (DataGrid)target;
			break;
		case 4:
			ProjectsDataGrid = (DataGrid)target;
			break;
		case 5:
			DocumentsDataGrid = (DataGrid)target;
			break;
		case 6:
			StatusTextBlock = (TextBlock)target;
			break;
		default:
			_contentLoaded = true;
			break;
		}
	}
}
