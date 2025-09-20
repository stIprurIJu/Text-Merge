import os
import glob
import chardet

def combine_text_files(folder_path, output_file_name="combined_output.txt"):
    """
    指定されたフォルダ内のすべてのテキストファイルを一つのファイルに結合します。
    異なる文字コードのファイルも自動的に検出してUTF-8に変換します。
    
    Args:
        folder_path (str): テキストファイルが含まれるフォルダのパス
        output_file_name (str): 結合されたテキストを保存するファイル名（デフォルト: combined_output.txt）
    """
    try:
        # 出力ファイルのパスを同じフォルダ内に設定
        output_file_path = os.path.join(folder_path, output_file_name)
        
        # フォルダ内のすべてのテキストファイルを取得
        text_files = glob.glob(os.path.join(folder_path, "*.txt"))
        
        # 出力ファイルを除外（既に存在する場合）
        text_files = [f for f in text_files if os.path.basename(f) != output_file_name]
        
        print(f"フォルダ内に{len(text_files)}個のテキストファイルが見つかりました")
        
        # 結合したコンテンツを保存する変数
        combined_content = ""
        
        # 各ファイルの内容を読み込んで結合
        for file_path in text_files:
            file_name = os.path.basename(file_path)
            
            # ファイルの文字コードを検出
            with open(file_path, 'rb') as rawfile:
                rawdata = rawfile.read()
                result = chardet.detect(rawdata)
                encoding = result['encoding']
            
            try:
                # 検出した文字コードでファイルを開いて内容を読み込む
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                
                print(f'"{file_name}" を読み込みました (文字コード: {encoding})')
            except UnicodeDecodeError:
                # 文字コード検出に失敗した場合、UTF-8で試行
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    print(f'"{file_name}" をUTF-8として読み込みました')
                except UnicodeDecodeError:
                    # それでも失敗した場合はエラーメッセージを表示して次のファイルへ
                    print(f'"{file_name}" の文字コードを検出できませんでした。このファイルはスキップします。')
                    continue
            
            # ファイル名をヘッダーとして追加
            combined_content += f"\n===== {file_name} (元の文字コード: {encoding}) =====\n\n"
            combined_content += content
            combined_content += "\n\n"
        
        # 結合したコンテンツを新しいファイルに書き込む
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(combined_content)
        
        print(f'すべてのテキストファイルを "{output_file_path}" に結合しました')
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def create_sample_files(folder_path):
    """
    テスト用のサンプルファイルを作成します。
    異なる文字コードのファイルも含めます。
    
    Args:
        folder_path (str): サンプルファイルを作成するフォルダのパス
    """
    try:
        # フォルダが存在しない場合は作成
        os.makedirs(folder_path, exist_ok=True)
        
        # UTF-8のサンプルファイルを作成
        with open(os.path.join(folder_path, 'file1.txt'), 'w', encoding='utf-8') as f:
            f.write('最初のファイルの内容です。\nこれはテスト用のテキストです。')
        
        # Shift-JISのサンプルファイルを作成
        with open(os.path.join(folder_path, 'file2.txt'), 'w', encoding='shift_jis') as f:
            f.write('2番目のファイルの内容です。\n複数行のテキストを含んでいます。')
        
        # EUC-JPのサンプルファイルを作成
        with open(os.path.join(folder_path, 'file3.txt'), 'w', encoding='euc_jp') as f:
            f.write('3番目のファイルです。\nこれで最後のサンプルファイルになります。')
        
        print('異なる文字コードのサンプルファイルを作成しました')
        
    except Exception as e:
        print(f"サンプルファイル作成中にエラーが発生しました: {e}")

if __name__ == "__main__":
    # 設定
    folder_path = r"C:\Users\bz_el\Desktop\files"  # 結合するファイルが含まれるフォルダのパス
    
    # サンプルファイルを作成してから結合を実行
    create_sample_files(folder_path)
    
    # 同じフォルダ内に結合結果を出力
    combine_text_files(folder_path, "combined_result.txt")