using System;
using System.CodeDom.Compiler;
using System.ComponentModel;
using System.Diagnostics;
using System.Security.Cryptography;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Markup;

namespace InsecureVault;

public class MainWindow : Window, IComponentConnector
{
	internal MainWindow window;

	internal StackPanel stackPanel;

	internal Image image;

	internal TextBox loginPasswordTBox;

	internal Button LoginButton;

	private bool _contentLoaded;

	public MainWindow()
	{
		InitializeComponent();
	}

	private static bool CheckPassword(string s)
	{
		if (s.Length != 45)
		{
			return false;
		}
		if (s.Substring(0, 4) != "ptm{")
		{
			return false;
		}
		using (MD5 mD = MD5.Create())
		{
			byte[] bytes = Encoding.UTF8.GetBytes(s.Substring(4, 4));
			if (BitConverter.ToString(mD.ComputeHash(bytes)).Replace("-", "").ToLower() != "33635414851f62863a5cb7825481433d")
			{
				return false;
			}
		}
		if (BitConverter.ToString(Encoding.UTF8.GetBytes(s.Substring(8, 4))).Replace("-", "").ToLower() != "5f345f46")
		{
			return false;
		}
		if (Convert.ToBase64String(Encoding.UTF8.GetBytes(s.Substring(12, 4))) != "dW5ueQ==")
		{
			return false;
		}
		string text = "0x" + ((int)s[19]).ToString("x");
		if (s[16] != '_' || (s[17] ^ 5) != 114 || s[18] != '4' || text != "0x79")
		{
			return false;
		}
		using (SHA256 sHA = SHA256.Create())
		{
			byte[] bytes2 = Encoding.UTF8.GetBytes(s.Substring(20, 4));
			if (BitConverter.ToString(sHA.ComputeHash(bytes2)).Replace("-", "").ToLower() != "c1cd3414aea97cfb005cf3bf3f39f3c1b5412f5dd8a2602c74a38181d94f5a2d")
			{
				return false;
			}
		}
		if (ToBase32String(Encoding.UTF8.GetBytes(s.Substring(24, 5))) != "MNUDGY3L")
		{
			return false;
		}
		string text2 = "0b" + Convert.ToString(s[30], 2);
		if (s[29] != '_' || text2 != "0b1100110" || s[31] != '0' || s[32] != 'R')
		{
			return false;
		}
		if (s.Substring(33, 3) != "_4_" || (int)s[36] >> 4 != 7)
		{
			return false;
		}
		int num = int.Parse(s[39].ToString());
		if ((s[37] ^ s[38]) != 1 || s[37] != '4' || num + 10 != 15 || s[40] != 'w')
		{
			return false;
		}
		if (BitConverter.ToString(Encoding.UTF8.GetBytes(s.Substring(41))).Replace("-", "").ToLower() != "3072647d")
		{
			return false;
		}
		return true;
	}

	private static string ToBase32String(byte[] bytes)
	{
		StringBuilder stringBuilder = new StringBuilder();
		int num = 0;
		int num2 = 0;
		foreach (byte b in bytes)
		{
			num = (num << 8) | b;
			num2 += 8;
			while (num2 >= 5)
			{
				num2 -= 5;
				stringBuilder.Append("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"[(num >> num2) & 0x1F]);
			}
		}
		if (num2 > 0)
		{
			stringBuilder.Append("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"[(num << 5 - num2) & 0x1F]);
		}
		while (stringBuilder.Length % 8 != 0)
		{
			stringBuilder.Append('=');
		}
		return stringBuilder.ToString();
	}

	private void LoginButton_Click(object sender, RoutedEventArgs e)
	{
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		if (CheckPassword(loginPasswordTBox.Text))
		{
			DbManager dbManager = new DbManager();
			Application.Current.MainWindow = (Window)(object)dbManager;
			((Window)dbManager).Show();
			((Window)this).Close();
		}
		else
		{
			MessageBox.Show("Incorrect password. Please try again.", "Login Failed", (MessageBoxButton)0, (MessageBoxImage)16);
		}
	}

	[DebuggerNonUserCode]
	[GeneratedCode("PresentationBuildTasks", "10.0.0.0")]
	public void InitializeComponent()
	{
		if (!_contentLoaded)
		{
			_contentLoaded = true;
			Uri uri = new Uri("/InsecureVault;component/mainwindow.xaml", UriKind.Relative);
			Application.LoadComponent((object)this, uri);
		}
	}

	[DebuggerNonUserCode]
	[GeneratedCode("PresentationBuildTasks", "10.0.0.0")]
	[EditorBrowsable(EditorBrowsableState.Never)]
	void IComponentConnector.Connect(int connectionId, object target)
	{
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0037: Expected O, but got Unknown
		//IL_003a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0044: Expected O, but got Unknown
		//IL_0047: Unknown result type (might be due to invalid IL or missing references)
		//IL_0051: Expected O, but got Unknown
		//IL_0054: Unknown result type (might be due to invalid IL or missing references)
		//IL_005e: Expected O, but got Unknown
		//IL_006b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0075: Expected O, but got Unknown
		switch (connectionId)
		{
		case 1:
			window = (MainWindow)target;
			break;
		case 2:
			stackPanel = (StackPanel)target;
			break;
		case 3:
			image = (Image)target;
			break;
		case 4:
			loginPasswordTBox = (TextBox)target;
			break;
		case 5:
			LoginButton = (Button)target;
			((ButtonBase)LoginButton).Click += new RoutedEventHandler(LoginButton_Click);
			break;
		default:
			_contentLoaded = true;
			break;
		}
	}
}
