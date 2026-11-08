<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="20008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">20.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str">LabVIEW 2026 Windows toast wrapper: direct composition and display through ToastBuilder, activation registration through ToastService, and an injected ActivationHandler for copied arguments and user-input values. Includes an interactive text-reply example. See README.md and CALLBACK-LIFETIME.md for ownership, shutdown and current limits.</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Development Examples" Type="Folder">
			<Item Name="Build Toast With Classes.vi" Type="VI" URL="../Development Examples/Build Toast With Classes.vi"/>
			<Item Name="Native Toast Example.vi" Type="VI" URL="../Development Examples/Native Toast Example.vi"/>
		</Item>
		<Item Name="ToastNotification.lvlib" Type="Library" URL="../ToastNotification/ToastNotification.lvlib"/>
		<Item Name="Toast Notifications for LabVIEW.vipb" Type="Document" URL="../Toast Notifications for LabVIEW.vipb"/>
		<Item Name="Microsoft.Toolkit.Uwp.Notifications.dll" Type="Document" URL="../bins/Microsoft.Toolkit.Uwp.Notifications.dll"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Recursive File List.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/Recursive File List.vi"/>
				<Item Name="List Directory and LLBs.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/libraryn.llb/List Directory and LLBs.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="To .NET Object.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/dotnet.llb/To .NET Object.vi"/>
			</Item>
			<Item Name="mscorlib" Type="VI" URL="mscorlib">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
